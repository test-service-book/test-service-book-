from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.company import Company


class CompanyResource(Resource):
    def get(self, id):
        abort_if_company_not_found(id)
        session = db_session.create_session()
        company = session.query(Company).get(id)
        return jsonify({'company': company.to_dict(
            only=('id', 'name', 'phone', 'location', 'INN', 'about') )})

    def delete(self, id):
        abort_if_company_not_found(id)
        session = db_session.create_session()
        company = session.query(Company).get(id)
        session.delete(company)
        session.commit()
        return jsonify({'success': 'OK'})


    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('phone')
        parser.add_argument('location')
        parser.add_argument('INN')
        parser.add_argument('about')

        args = parser.parse_args()
        session = db_session.create_session()


        company = session.query(Company).get(id)
        if not company:
            return abort(404, message=f"Company not found")

        if args['name']: company.name = args['name']
        if args['phone']: company.phone = args['phone']
        if args['location']: company.location = args['location']
        if args['INN']: company.INN = args['INN']
        if args['about']: company.about = args['about']

        session.commit()
        return jsonify({'success': 'OK'})



parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('location', required=True)
parser.add_argument('INN', required=True)



class CompanyListResource(Resource):
    def get(self):
        session = db_session.create_session()
        company = session.query(Company).all()
        return jsonify({'company': [item.to_dict(
            only=('id', 'name', 'phone')) for item in company]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        company = Company(
            name=args['name'],
            about=args['about'],
            phone=args['phone'],
            location=args['location'],
            INN=args['INN']
        )
        session.add(company)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_company_not_found(id):
    session = db_session.create_session()
    company = session.query(Company).get(id)
    if not company:
        abort(404, message=f"Company {id} not found")