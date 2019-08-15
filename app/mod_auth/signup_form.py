from flask_wtf import Form 

from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

class SignupForm(Form):

    first    = TextField('First Name', [Email(),
                Required()])

    last    = TextField('Last Name', [Email(),
                Required()])
            
    email    = TextField('Email Address', [Email(),
                Required()])

    password = PasswordField('Password', [
                Required()])