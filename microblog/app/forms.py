from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp

class ConditionForm(FlaskForm):
    condition = StringField('Treatment', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter your username")])
    # Password must have at least one upper, lower, capital, 
    password = PasswordField('Password', validators=[DataRequired("Please enter your password"), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired("Please enter a first name")])
    lastname = StringField('Last Name', validators=[DataRequired("Please enter a last name")])
    institution = StringField('Institution', validators=[DataRequired("Please enter a last name")])
    username = StringField('Username', validators=[DataRequired("Please enter a username")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password"), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')])
    submit = SubmitField('Register')