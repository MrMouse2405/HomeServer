from flask_wtf  import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError
from wtforms.validators import InputRequired,Length,EqualTo,AnyOf
from models import User, ADMIN_KEY
from passlib.hash import pbkdf2_sha512

def invalid_credentials(form,field):
    username_entered = form.username.data
    password_entered = field.data
    user_object = User.query.filter_by(username = username_entered).first()

    if user_object is None:
        raise ValidationError("Username/Password incorrect.")

    elif not pbkdf2_sha512.verify(password_entered,user_object.password):
        raise ValidationError("Username/Password incorrect.")

class RegistrationForm(FlaskForm):

    username = StringField('username_label',validators=[InputRequired(message='Username Required'),Length(min=1,max=20,message="Username must be between 1 to 20 chars")])
    password = PasswordField('pwd_field',validators=[InputRequired(message='Password Required'),Length(min=1,max=64,message="Password must be between 1 to 10 chars")])
    confirm_password = PasswordField('conf_pwd_label',validators=[InputRequired(message='Confirm Password'),EqualTo('password',message="Passwords Must match")])
    admin_key = PasswordField('admin_key_label',validators=[InputRequired(message='Admin Key'),AnyOf([ADMIN_KEY],message="Invalid Admin Key")])
    submit_button = SubmitField('Create')

    def validate_username(self,username):
        user_object = User.query.filter_by(username = username.data).first()
        if user_object:
            raise ValidationError("Username already exists.")

class LoginForm(FlaskForm):
    username = StringField('username_label',validators=[InputRequired(message='Required Username')])
    password = PasswordField('pwd_field',validators=[InputRequired(message='Password Required'),invalid_credentials ])
    submit_button = SubmitField('Login')
