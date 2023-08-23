from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.user import User


class UserResource(Resource):
    def get(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'phone', 'email', 'created_date', 'role'), )})

    def delete(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('phone')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('role')

        args = parser.parse_args()
        session = db_session.create_session()



        user = session.query(User).get(id)
        if not user:
            return abort(404, message=f"User not found")

        if args['name']: user.name = args['name']
        if args['phone']: user.phone = args['phone']
        if args['email']: user.email = args['email']
        if args['role']: user.email = args['role']
        if args['password']: user.set_password(args['password'])

        session.commit()
        return jsonify({'success': 'OK'})



parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('email', required=True)
parser.add_argument('about', required=True)
parser.add_argument('password', required=True)
parser.add_argument('role', required=True)



class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'name')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            phone=args['phone'],
            email=args['email'],
            about=args['about'],
            role=args['role']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")