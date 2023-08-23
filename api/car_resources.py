from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.car import Car
from  data.user import User

from api.functions import auth_key


parser = reqparse.RequestParser()
parser.add_argument('model', required=True)
parser.add_argument('millage', required=True)
parser.add_argument('year', required=True)
parser.add_argument('body_number', required=True)
parser.add_argument('engine_number', required=True)
parser.add_argument('owner_id', required=True)
parser.add_argument('state_number', required=True)
parser.add_argument('engine', required=True)
parser.add_argument('transmission', required=True)
parser.add_argument('drive_unit', required=True)
parser.add_argument('car_model_id', required=True)


class CarResource(Resource):

    # @auth_key # аутентификация
    def get(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        car = session.query(Car).get(id)
        return jsonify({'car': car.to_dict(
            only=('id', 'model', 'millage', 'year', 'body_number', 'engine_number', 'owner_id', 'state_number'), )})

    def delete(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        car = session.query(Car).get(id)
        session.delete(car)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('model')
        parser.add_argument('millage')
        parser.add_argument('year')
        parser.add_argument('body_number')
        parser.add_argument('engine_number')
        parser.add_argument('owner_id')
        parser.add_argument('state_number')
        parser.add_argument('engine')
        parser.add_argument('transmission')
        parser.add_argument('drive_unit')
        parser.add_argument('car_model_id')

        args = parser.parse_args()
        session = db_session.create_session()

        user = session.query(User).filter(User.id==args['owner_id'])
        if args['owner_id'] and  not user:
            return abort(404, message=f"Not found owner_id")

        car = session.query(Car).get(id)
        if not car:
            return abort(404, message=f"Car not found")

        if args['model']: car.model = args['model']
        if args['millage']: car.millage = args['millage']
        if args['year']: car.year = args['year']
        if args['body_number']: car.body_number = args['body_number']
        if args['engine_number']: car.engine_number = args['engine_number']
        if args['owner_id']: car.owner_id = args['owner_id']
        if args['state_number']: car.owner_id = args['state_number']
        if args['engine']: car.engine = args['engine']
        if args['transmission']: car.transmission = args['transmission']
        if args['drive_unit']: car.drive_unit = args['drive_unit']
        if args['car_model_id']: car.car_model_id = args['car_model_id']

        session.commit()
        return jsonify({'success': 'OK'})



class CarListResource(Resource):

    def get(self):
        session = db_session.create_session()
        car = session.query(Car).all()
        return jsonify({'car': [item.to_dict(
            only=('id', 'model', 'owner_id')) for item in car]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        user = session.query(User).get(args['owner_id'])
        if not user:
            return abort(404, message=f"Not found owner_id")

        car = Car(
            model=args['model'],
            millage=args['millage'],
            year=args['year'],
            body_number=args['body_number'],
            engine_number=args['engine_number'],
            owner_id=args['owner_id'],
            state_number = args['state_number'],
            engine = args['engine'],
            transmission = args['transmission'],
            drive_unit = args['drive_unit'],
            car_model_id = args['car_model_id']
        )

        session.add(car)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_not_found(id):
    session = db_session.create_session()
    car = session.query(Car).get(id)
    if not car:
        abort(404, message=f"Car {id} not found")