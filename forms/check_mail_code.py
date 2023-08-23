from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class CheckMailCode(FlaskForm):

    code = StringField("Код", validators=[DataRequired()])
    submit = SubmitField('Отправить')
