from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
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
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DiagnosisForm(FlaskForm):
    # This will be dynamic in the frontend with Checkboxes
    submit = SubmitField('Analyze Symptoms')

class AppointmentForm(FlaskForm):
    doctor = SelectField('Consultant Doctor', coerce=int, validators=[DataRequired()])
    date = DateField('Appointment Date', validators=[DataRequired()])
    time_slot = SelectField('Time Slot', choices=[
        ('09:00 AM', '09:00 AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'),
        ('02:00 PM', '02:00 PM'), ('03:00 PM', '03:00 PM'), ('04:00 PM', '04:00 PM')
    ], validators=[DataRequired()])
    submit = SubmitField('Book Appointment')
