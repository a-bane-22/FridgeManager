from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UserBase(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])


class RegistrationForm(UserBase):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')


class UserForm(UserBase):
    submit = SubmitField('Save User')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')


class DeleteUserForm(FlaskForm):
    confirm = BooleanField('Confirm')
    submit = SubmitField('Submit Selection')


class ItemForm(FlaskForm):
    upc = StringField('UPC', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    markdown = DateField('Markdown Date', validators=[DataRequired()])
    expiration = DateField('Expiration Date', validators=[DataRequired()])
    submit = SubmitField('Save Item')


class DateSearchForm(FlaskForm):
    date = DateField('Pick Date', validators=[DataRequired()])
    submit = SubmitField('Search Date')