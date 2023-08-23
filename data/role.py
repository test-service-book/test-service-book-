from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_security import RoleMixin
import sqlalchemy

class Role(SqlAlchemyBase, RoleMixin):
    __tablename__ = 'role'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)