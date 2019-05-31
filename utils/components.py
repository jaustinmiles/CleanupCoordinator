from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
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
