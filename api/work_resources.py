from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.work import Work
from data.car import Car
from data.company import Company
from data.worker import Worker
from data.characteristics import Characteristics


class WorkResource(Resource):
    def get(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        work = session.query(Work).get(id)
        return jsonify({'work': work.to_dict(
            only=('id', 'date', 'brand', 'amount', 'millage', 'company_id', 'car_id', 'worker_id', 'characteristic_id'), )})

    def delete(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        work = session.query(Work).get(id)
        session.delete(work)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('brand')
        parser.add_argument('amount')
        parser.add_argument('company_id')
        parser.add_argument('car_id')
        parser.add_argument('worker_id')
        parser.add_argument('characteristic_id')
        parser.add_argument('millage')

        args = parser.parse_args()
        session = db_session.create_session()

        if args['company_id'] and not session.query(Company).get(args['company_id']):
            return abort(404, message=f"Company is not found")
        if args['car_id'] and not session.query(Car).get(args['car_id']):
            return abort(404, message=f"Car is not found")
        if args['worker_id'] and not session.query(Worker).get(args['worker_id']):
            return abort(404, message=f"Worker is not found")
        if args['characteristic_id'] and not session.query(Characteristics).get(args['characteristic_id']):
            return abort(404, message=f"Characteristic is not found")

        work = session.query(Work).get(id)

        if args['brand']: work.brand = args['brand']
        if args['amount']: work.amount = args['amount']
        if args['company_id']: work.company_id = args['company_id']
        if args['car_id']: work.car_id = args['car_id']
        if args['worker_id']: work.worker_id = args['worker_id']
        if args['characteristic_id']: work.category_id = args['characteristic_id']
        if args['millage']: work.category_id = args['millage']

        session.commit()
        return jsonify({'success': 'OK'})



class WorkListResource(Resource):
    def get(self):
        session = db_session.create_session()
        work = session.query(Work).all()
        return jsonify({'work': [item.to_dict(
            only=('id', 'company_id', 'car_id', 'characteristic_id')) for item in work]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('brand', required=True)
        parser.add_argument('amount', required=True)
        parser.add_argument('company_id', required=True)
        parser.add_argument('car_id', required=True)
        parser.add_argument('worker_id', required=True)
        parser.add_argument('characteristic_id', required=True)
        parser.add_argument('millage', required=True)


        args = parser.parse_args()
        session = db_session.create_session()

        if not session.query(Company).get(args['company_id']):
            return abort(404, message=f"Company is not found")
        if not session.query(Car).get(args['car_id']):
            return abort(404, message=f"Car is not found")
        if not session.query(Worker).get(args['worker_id']):
            return abort(404, message=f"Worker is not found")
        if not session.query(Characteristics).get(args['characteristic_id']):
            return abort(404, message=f"Characteristic is not found")

        work = Work(
            brand=args['brand'],
            amount=args['amount'],
            company_id=args['company_id'],
            car_id=args['car_id'],
            worker_id=args['worker_id'],
            characteristic_id=args['characteristic_id'],
            millage=args['millage']
        )

        session.add(work)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_not_found(id):
    session = db_session.create_session()
    work = session.query(Work).get(id)
    if not work:
        abort(404, message=f"Work {id} not found")