from flask_wtf import FlaskForm 

from wtforms import TextField, PasswordField, FileField, BooleanField, SelectField
from wtforms.validators import Required

class ImportForm(FlaskForm):

    data_file = FileField('data_file')

    x = TextField('x_label')

    y = TextField('y_label')

    method = SelectField('method', choices=[('mean', 'ARMA'), ('arima', 'ARIMA'), ('ses', 'SES')])

    num_preds = TextField('num_preds')

    currency = BooleanField('currency')
