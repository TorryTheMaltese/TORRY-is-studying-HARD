from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo


class SignInForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired, Email])
    user_password = PasswordField('Password', validators=[DataRequired])


class SignUpForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired, Email])
    user_password = PasswordField('Password', validators=[DataRequired])
    user_repeat_password = PasswordField('Repeat Password', validators=[DataRequired, EqualTo('user_password')])
    user_name = StringField('Name', validators=[DataRequired])