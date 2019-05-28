import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from twilio.twiml.messaging_response import MessagingResponse

from utils.components import GenerateMembersButton, GenerateScheduleButton, AssignTasksButton

# Initial setup for the Flask app and migration capabilities of the database, along with the instantiation
# of the global variable db
basedir = os.path.abspath(os.path.dirname(__file__))
document_name = 'cleanup_sheet_test'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)
Migrate(app, db)


# Models


class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.Text)
    last = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    status = db.Column(db.Text)
    active = db.Column(db.Boolean)
    hours = db.Column(db.Integer)
    assigned = db.Column(db.Boolean)

    def __init__(self, first: str, last: str, phone: str, email: str, status: str, active: bool, hours, assigned=False):
        """
        Holds metadata and real data for members of the fraternity.
        Stored in the hours field is the running total of cleanup hours
        the member currently has. Default to -1 for work with exception
        handling
        :param first: first name of member
        :param last: last name of member
        :param phone: phone number of member
        :param email: email address of member
        :param status: whether the member is an Associate Member,
                       a Brother, or part of the Sayonara Squad (SS)
        :param active: whether the member is and active brother
        """
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.status = status
        self.active = active
        self.hours = hours
        self.assigned = assigned

    def __str__(self):
        return """Name: """ + self.first + ' ' + self.last \
               + """\nPhone: """ + str(self.phone) \
               + """\nEmail: """ + str(self.email) \
               + """\nStatus: """ + str(self.status) \
               + """\nActive: """ + str(self.active) \
               + """\nHours: """ + str(self.hours) + '\n'

    def member_status(self) -> int:
        """
        Simple mechanism to providing a comparable interface between members
        based on status. Lower number implies greater importance. To be used
        as a key in a lambda expression to perform sorting on lists of Members
        :rtype: int
        :return: integer equivalent of the status of the brother.
        """
        if self.status == 'SS':
            return 0
        elif self.status == 'NIB':
            return 2
        elif self.status == 'AM':
            return 3
        else:
            return 1


class CleanupHour(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    task_id = db.Column(db.Integer)
    day = db.Column(db.Text)
    due_time = db.Column(db.Text)
    worth = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    link = db.Column(db.Text)

    def __init__(self, name: str, task_id: int, day: str, due_time: str, worth: int, difficulty: int, link: str):
        """
        A CleanupHour holds the metadata and values for a cleanup task
        :param name: name of the task
        :param task_id: id to identify the task, used to load task descriptions
        :param day: due date of the task
        :param due_time: due time of the task
        :param worth: the cleanup-hour worth of completion of the task
        :param difficulty: estimated difficulty (scale of 1-5) of the task
        """
        self.name = name
        self.task_id = task_id
        self.day = day
        self.due_time = str(due_time)
        self.worth = worth
        self.difficulty = difficulty
        self.link = link

    def __str__(self):
        return """Name: """ + self.name \
               + """\nDue Date: """ + str(self.day) \
               + """\nDue Time: """ + str(self.due_time) \
               + """\nWorth: """ + str(self.worth) \
               + """\nLink: """ + str(self.link)
        # + """\nDifficulty: """ + str(self.difficulty) + '\n'
        # + """\nId: """ + str(self.task_id)\


class Assignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('cleanup_hour.id'))
    phone_number = db.Column(db.Text)
    response = db.Column(db.Text)

    def __init__(self, member_id: int, task_id: int, phone_number: str, response: str = 'Pending') -> None:
        """
        The assignment object represents the conjunction of a Member and a CleanupHour. They are connected by
        foreign keys (the task id and member id). The response (pending, confirm, or skip) is also recorded here,
        set as default to pending, and the phone number is kept here to easily identify the task upon response by
        phone.
        :rtype: None
        :param member_id: id of the Member object in the db
        :param task_id: id of the CleanupHour object in the db
        :param phone_number: phone number of the member of the assignment
        :param response: the member's response to the assignment
        """
        self.member_id = member_id
        self.task_id = task_id
        self.phone_number = phone_number
        self.response = response


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    The home page for the CleanupCoordinator. Includes a simple jumbotron for a welcome screen, along with
    links to the other pages, by extension from base.html
    :return: html template to render
    """
    return render_template('index.html')


@app.route('/members', methods=['GET', 'POST'])
def members():
    """
    page that contains all the members' data. Initially, it is blank. If the generate members button is
    pressed, then the MemberGenerator from modules will be used to utilize the Google API for generation
    of members from the provided document (document_name). If this happens, the user will be redirected to
    the same url, but the button will not be displayed, coherent to logic in members.html. After this is
    accomplished, the members will be stored in the database until it is reset.  Each member's name is also
    an anchor tag for his specific member page, which displays complete information.
    :return: template for members.html
    """
    generate = GenerateMembersButton()
    if generate.validate_on_submit():
        from modules.MemberGenerator import generate_members
        member_list = generate_members()
        db.session.add_all(member_list)
        db.session.commit()
        return redirect(url_for('members'))
    try:
        member_list = Member.query.all()
        member_list = sorted(member_list, key=lambda member: member.hours)
        member_list = [member for member in member_list if member.active]
    except Exception as e:
        print(e)
        member_list = []
    return render_template('members.html', generate=generate, member_list=member_list)


@app.route('/member/<identifier>')
def member_page(identifier):
    """
    page for a single member. Identifier corresponds to the unique database id, used to retrieve the member. Once
    the member is retrieved, it is passed into the html page for formatting using Jinja templating.
    :param identifier: unique db identifier
    :return: template for individual html page for member
    """
    member = Member.query.get(identifier)
    return render_template('member_page.html', member=member)


@app.route('/task/<identifier>')
def task_page(identifier):
    """
    similar to member_page, task_page is the page for a single task, containing all of its information.
    :param identifier: unique db identifier
    :return: template for individual task html
    """
    task = CleanupHour.query.get(identifier)
    return render_template('task_page.html', task=task)


@app.route('/assignment', methods=['GET', 'POST'])
def assignment():
    """
    Assignment represents the page for the user to generate the tasks from the google sheet, along with the button
    to link to final_assignments, where the task pairings are shown. If there are no tasks in the database, the generate
    tasks button must be pressed before the assign button, or nothing will happen. This page utilizes the
    CleanupHourScheduler to parse the document name passed in. Once this is done, the items are stored permanently in
    the database until reset.
    :return: template for assignment (the current page), or final_assignments (upon pressing the assign button)
    """
    generate = GenerateScheduleButton()
    try:
        hours_list = CleanupHour.query.all()
    except Exception as e:
        print(e)
        hours_list = []
    if generate.validate_on_submit() and not hours_list:
        from modules.CleanupHourScheduler import schedule_hours
        hours_list = schedule_hours()
        db.session.add_all(hours_list)
        db.session.commit()
        return redirect(url_for('assignment'))
    assign = AssignTasksButton()
    assignments = []
    if assign.validate_on_submit() and hours_list:
        return redirect(url_for('final_assignments'))

    return render_template('assignment.html', generate=generate, hours_list=hours_list, assign=assign,
                           assignments=assignments)


@app.route('/final_assignments', methods=['GET', 'POST'])
def final_assignments():
    """
    final assignments utilizes the Assigner object from modules.TaskAssigner to properly assign tasks according to
    difficulty and member status. The assigner is instantiated by first attempting to query both the members list
    and task_list from the db. If this is not possible, the lists will be set to empty and nothing will happen. At
    this point, the send_texts button will also do nothing and is safe to press. The user should clearly see, however,
    that there are no pairings and be alerted that one of the lists is invalid. If the querying is successful,
    the Assigner's assign_task() method will be run until assigner.finished is reached. Upon this point, a successful
    list of assignments should be present in assignments, and this list will be passed into the template for
    final_assignments.html for tabular formatting.

    If the send_texts button is pressed with valid lists, the assignments will be formalized, and Assignment objects
    will be created and committed to the db. The user will then be redirected to text_report.html

    There is also the option to remove a member manually from the assignments. The button ids are in the form of
    'remove_<member id>', so using button[7:] retrieves the id from the button. This member is then marked as assigned

    :return: template for final_assignments or text_report (upon button press)
    """
    from modules.TaskAssigner import get_assigner
    # if the reassign button was pressed
    if request.method == 'POST':
        button_ids = request.values.keys()
        for button_id in button_ids:
            if 'remove_' in button_id:
                member_id = int(button_id[7:])
                member = Member.query.get(member_id)
                member.assigned = True
                db.session.add(member)
                db.session.commit()
    # try to query lists, set to empty if exception
    try:
        member_list = Member.query.all()
        hours_list = CleanupHour.query.all()
    except Exception as e:
        print(e)
        member_list = []
        hours_list = []
    assignments = []
    # try to create assignments, otherwise, set assignments to empty so that pressing the send_texts button is safe
    if member_list and hours_list:
        assigner = get_assigner(member_list, hours_list)
        successful_assignment = True
        while not assigner.finished:
            try:
                pair = assigner.assign_task()
                assignments.append(pair)
            except Exception as e:
                print(e)
                print('There was an error with assigning tasks. Make sure both lists are valid')
                successful_assignment = False
                break
        if not successful_assignment:
            hours_list = []
            assignments = []
    if request.method == 'POST':
        button_ids = request.values.keys()
        for button_id in button_ids:
            if 'send_texts' in button_id:
                for assign in assignments:
                    phone = assign[0].phone
                    phone_fixed = '+1' + ''.join([char for char in phone if char != '-'])
                    db_pair = Assignment(assign[0].id, assign[1].id, phone_fixed)
                    db.session.add(db_pair)
                    member = Member.query.get(assign[0].id)
                    member.assigned = True
                    db.session.add(member)
                    db.session.commit()
                return redirect(url_for('text_report', assignments=assignments))

    enumerated = range(len(assignments))

    return render_template('final_assignments.html', hours_list=hours_list, assignments=assignments,
                           enumerated=enumerated)


@app.route('/text_report', methods=['GET', 'POST'])
def text_report():
    """
    The text_report tries to retrieve assignments from the database for use with the TextClient module. For each
    assignment, the Member and CleanupHour objects are queried from the db and passed into the text_assigner's
    send_assignment() method. The text report is then rendered.
    :return: template for the text report
    """
    from modules.TextClient import initialize_text_assigner
    try:
        text_assigner = initialize_text_assigner()
        assignments = Assignment.query.all()
        for assign in assignments:
            pair = (Member.query.get(assign.member_id), CleanupHour.query.get(assign.task_id))
            text_assigner.send_assignment(pair)
    except Exception as e:
        print(e)
        print('There was an error with sending the text to the member')
    return render_template('text_report.html')


@app.route('/assignment_status', methods=['GET', 'POST'])
def assignment_status():
    """
    The assignment status page is responsible for reporting the results of the member-cleanup hour assignments. The
    results correspond to the status of the response (pending, confirm, or skip). From the assignments, a member list
    and a task list are created for use in the templating (to create a table from the lists).
    :return: template for the assignment status, formatted using the members, tasks, and assignments lists
    """
    assignments = Assignment.query.all()
    members_list = []
    tasks = []
    try:
        for assign in assignments:
            member = Member.query.get(assign.member_id)
            task = CleanupHour.query.get(assign.task_id)
            members_list.append(member)
            tasks.append(task)
    except Exception as e:
        print(e)
        print('There was a problem generating member-cleanup hour pairs from the assignments in the database')
    # enumerated is for use with jinja templating
    enumerated = range(len(assignments))
    return render_template('assignment_status.html', members=members_list, tasks=tasks, assignments=assignments,
                           enumerated=enumerated)


@app.route("/sms", methods=['GET', 'POST'])
def reply():
    """
    Responds to a text message. Instantiates text client to receive messages list. The most recent message
    is the one that it will respond to. It will then go through the various cases and log the response.
    If the response is a skip, the skip handler will be called.
    """
    body = request.values.get('Body', None)
    number = request.values.get('From', None)
    resp = MessagingResponse()
    # try to query the response. If the query fails, respond with an appropriate message
    try:
        assign = Assignment.query.filter_by(phone_number=number).first()
        # if the member has already responded
        if assign.response != 'Pending':
            resp.message('Sorry, looks like you''ve already responded. If you need to change your response,'
                         + ' please message the housing manager.')
            return str(resp)
    except Exception as e:
        print(e)
        resp.message('Oops, it looks like you have not been assigned a cleanup hour!')
        return str(resp)
    number_no_1 = number[1:]
    from modules import SkipHandler
    if 'confirm' in body.lower():
        assign.response = 'Confirm'
        resp.message("Thank you for your confirmation. Details will be sent out shortly")
    elif 'skip' in body.lower():
        assign.response = 'Skip'
        resp.message("Sorry you had to skip. We'll get you next time")
        SkipHandler.reassign(number, number_no_1)
    else:
        resp.message("The message you sent was not a valid option. Please try again")
    db.session.add(assign)
    db.session.commit()
    return str(resp)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """
    Easy button click function to clear the entire database at the beginning of each week. When this happens, all
    data stored in Members, Assignments, and CleanupHours will be erased, but no information stored in the excel sheet
    will be touched.
    :return: template for delete.html
    """
    if request.method == 'POST':
        button_ids = request.values.keys()
        for button_id in button_ids:
            if 'delete_all' in button_id:
                members_list = Member.query.all()
                for member in members_list:
                    db.session.delete(member)
                tasks = CleanupHour.query.all()
                for task in tasks:
                    db.session.delete(task)
                assignments = Assignment.query.all()
                for assign in assignments:
                    db.session.delete(assign)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)