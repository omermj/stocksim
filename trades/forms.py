from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class NewTradeForm(FlaskForm):
    """Form for placing a new trade"""

    symbol = StringField("Symbol", validators=[DataRequired(), Length(max=10)])
    type = RadioField("Type", choices=[("buy", "Buy"), ("sell", "Sell")], default="buy")
    qty = IntegerField("Quantity", validators=[DataRequired()])
