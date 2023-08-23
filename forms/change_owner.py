from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired


class ChangeOwner(FlaskForm):

    car = SelectField("Автомобиль", validators=[DataRequired()])
    user = StringField("Код от нового владельца", validators=[DataRequired()])

    submit = SubmitField('Изменить')
