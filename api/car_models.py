from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.car_models import CarModels


class CarModelsResource(Resource):

    def get(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        carmodels = session.query(CarModels).filter(CarModels.mark_id == id).all()
        return jsonify({'car_models': [car.to_dict(only=('id', 'name')) for car in carmodels]})

#     def delete(self, id):
#         abort_if_not_found(id)
#         session = db_session.create_session()
#         car = session.query(Car).get(id)
#         session.delete(car)
#         session.commit()
#         return jsonify({'success': 'OK'})
#
#     def put(self, id):
#
#         parser = reqparse.RequestParser()
#         parser.add_argument('model')
#         parser.add_argument('millage')
#         parser.add_argument('year')
#         parser.add_argument('body_number')
#         parser.add_argument('engine_number')
#         parser.add_argument('owner_id')
#         parser.add_argument('state_number')
#
#         args = parser.parse_args()
#         session = db_session.create_session()
#
#         user = session.query(User).get(args['owner_id'])
#         if args['owner_id'] and  not user:
#             return abort(404, message=f"Not found owner_id")
#
#         car = session.query(Car).get(id)
#         if not car:
#             return abort(404, message=f"Car not found")
#
#         if args['model']: car.model = args['model']
#         if args['millage']: car.millage = args['millage']
#         if args['year']: car.year = args['year']
#         if args['body_number']: car.body_number = args['body_number']
#         if args['engine_number']: car.engine_number = args['engine_number']
#         if args['owner_id']: car.owner_id = args['owner_id']
#         if args['state_number']: car.owner_id = args['state_number']
#
#         session.commit()
#         return jsonify({'success': 'OK'})
#
#
#
# class CarListResource(Resource):
#
#     def get(self):
#         session = db_session.create_session()
#         car = session.query(Car).all()
#         return jsonify({'car': [item.to_dict(
#             only=('id', 'model', 'owner_id')) for item in car]})
#
#     def post(self):
#         args = parser.parse_args()
#         session = db_session.create_session()
#
#         user = session.query(User).get(args['owner_id'])
#         if not user:
#             return abort(404, message=f"Not found owner_id")
#
#         car = Car(
#             model=args['model'],
#             millage=args['millage'],
#             year=args['year'],
#             body_number=args['body_number'],
#             engine_number=args['engine_number'],
#             owner_id=args['owner_id'],
#             state_number = args['state_number']
#         )
#
#         session.add(car)
#         session.commit()
#         return jsonify({'success': 'OK'})



def abort_if_not_found(id):
    session = db_session.create_session()
    carmodels = session.query(CarModels).get(id)
    if not carmodels:
        abort(404, message=f"CarModel {id} not found")