import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
import datetime


class CarCode(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'carcode'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=True)
    car_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("car.id"), nullable=True, unique=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    car = orm.relationship('Car')


