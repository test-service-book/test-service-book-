from sqlalchemy.orm import Session
from flask_login import current_user
from flask import abort

class Security():
    def __init__(self, user_model, role_model, rolesusers, conn:Session):
        self.user = user_model
        self.role = role_model
        self.rolesusers = rolesusers
        self.conn = conn

        self.config = {'ACCESS_DENIED_URL' : '/404'}


    def role_required(self, dec_role):

        def dec(func):

            def f(*args, **kwargs):
                nonlocal dec_role
                role = self.conn.query(self.role).filter(self.role.name == dec_role).first()
                user = self.conn.query(self.user).filter(self.user.id == current_user.id).first()

                if any(r.id == role.id for r in user.roles):
                    return func(*args, **kwargs)
                else:
                    return abort(403)

            # декорированная функция не может быть одного имени с другими обработчиками страниц
            f.__name__ = func.__name__
            return f

        return dec

    def set_role(self, user:int, role:str):

        ru = self.rolesusers(
            user_id=user.id,
            role_id=self.conn.query(self.role).filter(self.role.name == role).first().id
        )
        self.conn.add(ru)
        self.conn.commit()