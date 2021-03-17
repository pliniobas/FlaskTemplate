from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import Users
import sys

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(),Length(min=6, max=16)] )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(),Length(min=6, max=16)])
    password_confirm = PasswordField("Confirm Password", validators = [DataRequired(),Length(min=6, max=16),EqualTo('password')])
    first_name = StringField("First Name", validators = [DataRequired(),Length(min=2, max=55)])
    last_name = StringField("Last Name", validators = [DataRequired(),Length(min=2, max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self,email):
        # print('---------------------email',email)
        # print('---------------------type(email)',type(email))
        # print('---------------------email.value',email.data)
        # print('---------------------dir(email)',dir(email))
        # sys.exit()
        user = Users.query.filter_by(email = email.data).first() #Essa query do SQL retorna o usuario 
        print('----------------- user',user)
        if user:
            raise ValidationError("Email is already in use. Pick another one.")
