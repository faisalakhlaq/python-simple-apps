from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, TextAreaField
from wtforms.validators import Required, ValidationError


class AmountIntValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u'Amount must be an integer value greater than 0.'
        self.message = message

    def __call__(self, form, field):
        if not field.data or not isinstance(field.data, int) or int(field.data) == 0:
            raise ValidationError(self.message)


class CryptoFetcherForm(FlaskForm):
    currency_symbol = StringField('Crypto Currency Symbol', validators=[Required()])
    amount = IntegerField('Amount', validators=[AmountIntValidator()])
    add_currency = SubmitField('Add Currency')
    currencies = TextAreaField('Added Currencies')
    # currencies = TextAreaField('Added Currencies', render_kw={'class': 'currencies-textarea', 'rows': 5})
    fetch_data = SubmitField('View Portfolio')
