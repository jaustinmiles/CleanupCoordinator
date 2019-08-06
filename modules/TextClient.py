from twilio.rest import Client
from modules import CleanupHourScheduler
from modules import MemberGenerator
from modules import TaskAssigner


class TextAssigner:

    def __init__(self):
        """
        The TextAssigner tethers the application to the Twilio text service. It houses the
        Client that has the capability of creating and sending messages, and it has the phone
        number of the text service (the number texts will be sent from).
        """
        token = open('modules/twilio_token.txt').readline().strip()
        account_sid = open('modules/twilio_account.txt').readline().strip()
        client = Client(account_sid, token)
        self.client = client
        self.phone = "+14702020929"

    def send_assignment(self, task_assignment: tuple, assignment_id) -> None:
        """
        Takes in a task_assignment tuple, usually received by the Assigner from TaskAssigner.
        Given this task, send_assignment will open the template text message file and append the
        str() representation of the Task to it. It also filters the phone numbers to alter them
        to Twilio format. The client will then send this message to the recipient
        :param assignment_id: provided to add a verification submission token (the id itself) to the cleanup task.
        :param task_assignment: (Member, CleanupHour) tuple
        """
        member = task_assignment[0]
        task = task_assignment[1]
        phone = member.phone
        phone_fixed = '+1' + str([char for char in phone if char != '-'])
        file = open('static/text_template.txt')
        line = file.readline()
        text = line + '\n\n' + str(task)
        text = text + '\n\n Your submit token is ' + str(assignment_id)
        file.close()
        self.client.messages.create(
            to=phone_fixed,
            from_=self.phone,
            body=text)

    def send_reminders(self, member_list):
        for member in member_list:
            phone = member.phone
            phone_fixed = '+1' + str([char for char in phone if char != '-'])
            file = open('static/reminder_template.txt')
            line = file.readline().strip()
            file.close()
            self.client.messages.create(
                to=phone_fixed,
                from_=self.phone,
                body=line)


def initialize_text_assigner() -> TextAssigner:
    """
    Simple function call to initialize a TextAssigner
    :rtype: TextAssigner
    :return: an instance of the TextAssigner
    """
    return TextAssigner()


if __name__ == '__main__':
    tasks = CleanupHourScheduler.schedule_hours()
    members = MemberGenerator.generate_members()
    assigner = TaskAssigner.Assigner(members, tasks)
    task_tup = assigner.assign_task()
    text_assigner = initialize_text_assigner()
    text_assigner.send_assignment((task_tup[0], task_tup[1]), 1)
    # TaskLogger.log_task((task_tup[1], task_tup[0]))
