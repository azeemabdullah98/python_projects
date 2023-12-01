from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, EmailField, PasswordField, SubmitField, BooleanField,
                      TextAreaField, IntegerField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from commercial_app.models import User, Admin

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists. Please try another username")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                "Email already exists. Please try anothe Email")

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    client_secret = PasswordField('Enter client secret',validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Admin.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists. Please try another username")

    def validate_email(self, email):
        email = Admin.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                "Email already exists. Please try anothe Email")


class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    client_secret = PasswordField('client_secret',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture = FileField('Upload Design Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    tags = TextAreaField('Tags', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Upload')
