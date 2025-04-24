from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators

class LoginForm(FlaskForm):
    username = StringField( label="", validators=[validators.DataRequired("Username is missing")] )
    password = PasswordField( label="", validators=[validators.DataRequired("Password is missing")] )
    remember_me = BooleanField( label="Remember Me" )
    submit = SubmitField( label="Sign In" )
    