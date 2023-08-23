from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired


class AddSelfWorkForm(FlaskForm):

    brand = StringField("Наименование", validators=[DataRequired()])
    amount = StringField("Количество", validators=[DataRequired()])
    millage = StringField("Пробег", validators=[DataRequired()])
    characteristic = SelectField("Категория", validators=[DataRequired()])
    car = SelectField("Категория", validators=[DataRequired()])

    submit = SubmitField('Добавить')
