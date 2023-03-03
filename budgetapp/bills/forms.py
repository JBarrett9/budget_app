from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class AddBillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    amount = DecimalField('Amount')
    due = DateField('Due', validators=[DataRequired()])
    recurring = BooleanField('Recurring')
    fixed_amt = BooleanField('Fixed amount')
    frequency = SelectField('Frequency', choices=[('once', 'Once'), ('weekly', 'Weekly'), ('bi-weekly', 'Bi-Weekly'),
                                                  ('monthly', 'Monthly'), ('bi-monthly', 'Bi-Monthly'),
                                                  ('yearly', 'Yearly')])
    submit = SubmitField('Add')
