from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired


class AddWorkerForm(FlaskForm):

    name = StringField("Имя", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired()])
    about = StringField("О себе", validators=[DataRequired()])

    submit = SubmitField('Добавить')
