from flask_wtf import FlaskForm
from wtforms import SubmitField


class GenerateMembersButton(FlaskForm):
    submit = SubmitField('Click here to pull members from the google spreadsheet.')


class GenerateScheduleButton(FlaskForm):
    submit = SubmitField('Click here to pull the schedule from the google spreadsheet.')


class AssignTasksButton(FlaskForm):
    submit = SubmitField('Assign Tasks')
