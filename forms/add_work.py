from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired


class AddWorkForm(FlaskForm):

    brand = StringField("Наименование", validators=[DataRequired()])
    amount = StringField("Количество", validators=[DataRequired()])
    millage = StringField("Пробег", validators=[DataRequired()])
    characteristic = SelectField("Категория", validators=[DataRequired()])
    worker = SelectField("Работник", validators=[DataRequired()])
    code = StringField("Код пользователя", validators=[DataRequired()])


    submit = SubmitField('Добавить')
