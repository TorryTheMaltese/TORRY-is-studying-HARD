from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User, Post
from flask_login import current_user

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


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
    post_title = StringField('Title', validators=[DataRequired()])
    post_image = FileField('Image', validators=[FileRequired()])
    post_image_name = StringField('Image Name', validators=[DataRequired])
    post_image_path = StringField('Image Path', validators=[DataRequired])
