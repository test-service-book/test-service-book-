import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class OtherWork(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'otherwork'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    millage = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("company.id"))
    car_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("car.id"))
    worker_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("worker.id"))

    company = sqlalchemy.orm.relationship('Company')
    car = sqlalchemy.orm.relationship('Car')
    worker = sqlalchemy.orm.relationship('Worker')
