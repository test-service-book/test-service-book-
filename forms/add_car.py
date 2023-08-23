from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from datetime import datetime

class AddCarForm(FlaskForm):

    # def year_check(form, field):
    #     if not(1900 < int(field.data) <= datetime.now().year):
    #         raise ValidationError('Введите корректную дату')



    mark = SelectField("Марка автомобиля", validators=[DataRequired()])
    model = SelectField("Модель автомобиля", validators=[DataRequired()])
    engine = SelectField("Тип двигателя", validators=[DataRequired()])
    transmission = SelectField("Трансмиссия", validators=[DataRequired()])
    drive_unit = SelectField("Тип привода", validators=[DataRequired()])
    # три поля выше временные, до того, пока не будет добавлена общая таблица автомобилей
    millage = IntegerField("Пробег", validators=[DataRequired()])
    year = IntegerField("Год", validators=[DataRequired(), NumberRange(min=1900, max=int(datetime.now().year), message='Введите корректную дату')])
    body_number = StringField("Номер кузова", validators=[DataRequired()])
    engine_number = StringField("Номер двигателя", validators=[DataRequired()])
    state_number = StringField("Гос номер", validators=[DataRequired()])

    submit = SubmitField('Добавить')


