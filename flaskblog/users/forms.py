from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Логін',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Пошта',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Пароль',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердіть пароль',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватись')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Користувач вже існує, оберіть інший нікнейм')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пошта вже зареєстрована, оберіть іншу!')

class LoginForm(FlaskForm):
    #username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    #confirm_password = PasswordField('Confirm password',
    #                        validators=[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign Up')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    picture = FileField('Update Profile picture',
                            validators=[FileAllowed(['jpg', 'png', 'tif'])])
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('User is already exist. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already exist. Please choose a different one')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with such email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')