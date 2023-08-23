import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class CarModels(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'car_models'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    mark_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("car_marks.id"))

    mark = orm.relationship('CarMarks')