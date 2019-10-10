from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User
from flask_login import current_user


class SignInForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    user_remember_me = BooleanField('Remember Me')


class SignUpForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    user_repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('user_password')])
    user_name = StringField('Name', validators=[DataRequired()])

    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')


class EditUserForm(FlaskForm):
    user_email = StringField('E-Mail')
    user_password = PasswordField('Password', validators=[DataRequired()])
    user_name = StringField('Name')

    def validate_user_email(self, user_email):
        if user_email.data == current_user.user_email:
            raise ValidationError('Please enter a different email address!!')

        user = User.query.filter_by(user_email=user_email.data).first()
        if user:
            raise ValidationError('Please enter a different email address!!')


class UploadForm(FlaskForm):
    board_title = StringField('Title', validators=[DataRequired()])
    board_image = StringField('Image', validators=[DataRequired()])
