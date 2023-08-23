from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.worker import Worker
from data.company import Company


class WorkerResource(Resource):
    def get(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        worker = session.query(Worker).get(id)
        return jsonify({'user': worker.to_dict(
            only=('id', 'name', 'phone', 'about', 'company.name'), )})

    def delete(self, id):
        abort_if_not_found(id)
        session = db_session.create_session()
        worker = session.query(Worker).get(id)
        session.delete(worker)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('phone')
        parser.add_argument('about')
        parser.add_argument('company_id')

        args = parser.parse_args()
        session = db_session.create_session()

        company = session.query(Company).get(args['company_id'])
        if args['company_id'] and not company:
            return abort(404, message=f"Not found company_id")

        worker = session.query(Worker).get(id)
        if not worker:
            return abort(404, message=f"Worker not found")

        if args['name']: worker.name = args['name']
        if args['phone']: worker.phone = args['phone']
        if args['about']: worker.about = args['about']
        if args['company_id']: worker.company_id = args['company_id']

        session.commit()
        return jsonify({'success': 'OK'})



parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('about', required=True)
parser.add_argument('company_id', required=True)


class WorkerListResource(Resource):
    def get(self):
        session = db_session.create_session()
        worker = session.query(Worker).all()
        return jsonify({'worker': [item.to_dict(
            only=('id', 'name', 'phone')) for item in worker]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        worker = Worker(
            name=args['name'],
            phone=args['phone'],
            company_id=args['company_id'],
            about=args['about']
        )

        session.add(worker)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_not_found(id):
    session = db_session.create_session()
    worker = session.query(Worker).get(id)
    if not worker:
        abort(404, message=f"Worker {id} not found")