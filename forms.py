from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddProblemForm(FlaskForm):
    name = StringField('name',
                        validators=[DataRequired(), Email()])
    statement = TextAreaField('statement', validators=[DataRequired()])
    sample_input=TextAreaField('Sample input',
                        validators=[DataRequired()])
    sample_output=TextAreaField('Sample output',
                        validators=[DataRequired()])
    submit = SubmitField('Submit Problem to review')