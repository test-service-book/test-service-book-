from flask_mail import Mail, Message
from settings import URL, MAIL_REG_CODE, MAIL_SUPPORT


class MailSender:
    def __init__(self, app):
        self.mail = Mail(app)
        self.app = app

    def send_registration_code(self, user_mail, hash, code):
        msg = Message("Завершение регистрации", sender=MAIL_REG_CODE,
                      recipients=[user_mail])

        msg.html = f"""
            Вы подали заявку на регистрацию.<br> 
            Для завершения регистрации пройдите по 
            <a href='{URL}/check_code?hash={hash}&code={code}'>{URL}/check_code?hash={hash}&code={code}</a> или 
            введите код на странице регистрации.
            <h2>Код: {code}</h2>"""

        self.mail.send(msg)
        return True

    def send_support_message(self, user_mail: str, subject: str, text: str, fio: str, link: str):
        msg = Message('User_message: ' + subject, sender=MAIL_SUPPORT,
                      recipients=[MAIL_SUPPORT])

        msg.html = f"""
                    Сообщение от пользователя {fio} ({user_mail})<br>
                    Текст:<br>
                    {text} <br>
                    Произошло на странице {link}
                    """

        self.mail.send(msg)
        return True
