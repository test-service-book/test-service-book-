from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired


class RegCompanyForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    about = TextAreaField('О компании', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    location = StringField('Адрес', validators=[DataRequired()])
    INN = StringField('ИНН', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    submit = SubmitField('Подать заявку')