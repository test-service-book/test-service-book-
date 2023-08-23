from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

class ChooseForEdit(FlaskForm):

    mark = SelectField("Марка автомобиля", validators=[DataRequired()])
    model = SelectField("Модель автомобиля", validators=[DataRequired()])

    submit = SubmitField('Выбрать')


