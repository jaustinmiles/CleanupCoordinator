from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email


class GenerateMembersButton(FlaskForm):
    submit = SubmitField('Click here to pull members from the google spreadsheet.')


class GenerateScheduleButton(FlaskForm):
    submit = SubmitField('Click here to pull the schedule from the google spreadsheet.')


class AssignTasksButton(FlaskForm):
    submit = SubmitField('Assign Tasks')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


def get_member_choices():
    from app import Member
    members = Member.query.all()
    member_choices = []
    for member in members:
        member_choices += [(str(member.id), member.first + ' ' + member.last)]
    return member_choices


def get_task_choices():
    from app import CleanupHour
    tasks = CleanupHour.query.all()
    task_choices = []
    for task in tasks:
        task_choices += [(str(task.id), task.name)]
    return task_choices


class SubmitHourForm(FlaskForm):
    name = SelectField("What is your name?", choices=get_member_choices())
    hour = SelectField("What hour did you do?", choices=get_task_choices())
    token = StringField("What is your assignment token?", validators=[DataRequired()])
    submit = SubmitField('Submit')


