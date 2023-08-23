import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Company(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'company'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    INN = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), nullable=True)

    user = sqlalchemy.orm.relationship('User')

'''
при инициализации бд должна создаваться запись с id=1, 
эта компания для установки первоначального пробега
так же нужно создать работника, для этой компании

кроме этого нужно создать компанию для самостоятельного проведения тех обслуживания
ЭТО ПОКА НЕ РЕАЛИЗОВАНО

'''
