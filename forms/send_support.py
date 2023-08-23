from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class SendSupport(FlaskForm):
    subject = StringField('Тема обращения', validators=[DataRequired()])
    text = TextAreaField('Ваш вопрос', validators=[DataRequired()])
    fio = StringField('Ваши ФИО', validators=[DataRequired()])
    email = EmailField('Email для связи', validators=[DataRequired()])
    link = StringField("Ссылка на страницу, на которой возникли сложности")
    agreement = BooleanField('Я даю свое согласие на обработку моих персональных данных', validators=[DataRequired()])

    submit = SubmitField('Отправить')