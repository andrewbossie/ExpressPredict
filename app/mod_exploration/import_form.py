from flask_wtf import FlaskForm 

from wtforms import TextField, PasswordField, FileField, BooleanField
from wtforms.validators import Required

class ImportForm(FlaskForm):

    data_file = FileField('data_file')

    x = TextField('x_label')

    y = TextField('y_label')

    currency = BooleanField('currency')
