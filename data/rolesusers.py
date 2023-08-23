from .db_session import SqlAlchemyBase
import sqlalchemy

class RolesUsers(SqlAlchemyBase):
    __tablename__ = 'roles_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('role.id'))