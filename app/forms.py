from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms import validators
from app import db
from app.models import User
import sqlalchemy as sa


class LoginForm(FlaskForm):
    username = StringField( label="Username", validators=[validators.DataRequired("Username is missing")] )
    password = PasswordField( label="Password", validators=[validators.DataRequired("Password is missing")] )
    remember_me = BooleanField( label="Remember Me" )
    submit = SubmitField( label="Sign In" )

# registration form for application

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired('Username is missing!')])
    email = StringField('Email', validators=[validators.DataRequired('Email is missing'), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired('Password is required')])
    password_confirm = PasswordField(
        label='Confirm Password',
        validators=[validators.DataRequired(), validators.EqualTo('password')]
    )
    submit = SubmitField('Sign Up')
    
    # check that usename is not taken
    def validate_username(self, username):
        user = db.session.scalar( 
                                sa
                                .select(User)
                                .where(User.username==username.data)
                                )
        if user is not None:
            raise ValidationError("Please use a different Username")
            
    
    # check the db to ensure email isnt taken
    def validate_email(self,email):
        user = db.session.scalar(sa
                                .select(User)
                                .where(User.email==email.data)
                                )
        
        if user is not None:
            raise ValidationError("Please use a different Email Address")
