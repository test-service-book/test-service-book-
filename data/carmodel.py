import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class CarModel(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'carmodel'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    model = sqlalchemy.Column(sqlalchemy.String, nullable=True)



    transmission = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # 0 - МКПП, 1 - АКПП

    drive_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # 0 - задний привод, 1 - передний привод

    tank_volume = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    oil_engine_volume = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    oil_transmission_volume = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    oil_drive_volume = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    tire_pressure = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    collant_volume = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)



