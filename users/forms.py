from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, RadioField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class ChangeAccountSettings(FlaskForm):
    """Form to withdraw/deposit funds"""

    type = RadioField("Transaction", choices=[
                      ("deposit", "Deposit"), ("withdraw", "Withdraw")], default="deposit")
    amount = FloatField("Amount", validators=[DataRequired(message="Amount can only be between 1 and 1,000,000"),
                                              NumberRange(min=1, max=1000000,
                                                          message="Amount can only be between 1 and 1,000,000")])
