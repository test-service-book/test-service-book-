import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

class Work(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'work'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    brand = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    millage = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("company.id"))
    car_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("car.id"))
    worker_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("worker.id"))

    characteristic_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("characteristics.id"))

    company = orm.relationship('Company')
    car = orm.relationship('Car')
    worker = orm.relationship('Worker')
    characteristics = orm.relationship('Characteristics')

    category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("category.id"))
    # TODO category_id нужно удалить, лишнее поле и таблица