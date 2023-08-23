import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Car(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'car'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    model = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    millage = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    body_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    engine_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    state_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship('User')

    car_model_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("car_models.id"))
    car_models = orm.relationship('CarModels')

    # три поля пока нет таблиц с полной информацией об авто
    engine = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    transmission = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    drive_unit = sqlalchemy.Column(sqlalchemy.Integer, default=0)


    def get_name(self):
        return f'{self.car_models.mark.name} {self.car_models.name}'




