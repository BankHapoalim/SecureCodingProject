from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UploadCheckForm(FlaskForm):
    photo = FileField('Check Photo', validators=[DataRequired()])
    password = PasswordField('Password in case of archive with password')
    amount = FloatField('Amount', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])

class UploadDigitallySignedCheckForm(FlaskForm):
    signedCheck = FileField('Signed Check File', validators=[DataRequired()])

class GetCheckStatusForm(FlaskForm):
    check_id = IntegerField('Check ID', validators=[DataRequired()])
    submit = SubmitField('Check Status')

class DeleteCheckForm(FlaskForm):
    check_id = IntegerField('Check ID', validators=[DataRequired()])
    submit = SubmitField('Delete Check')

