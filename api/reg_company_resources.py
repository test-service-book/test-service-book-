from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.reg_company import RegCompany


class RegCompanyResource(Resource):
    def get(self, id):
        abort_if_company_not_found(id)
        session = db_session.create_session()
        regcompany = session.query(RegCompany).get(id)
        return jsonify({'reg_company': regcompany.to_dict(
            only=('id', 'name', 'phone', 'location', 'INN', 'about', 'created_date', 'accepted', 'email', 'hashed_password') )})

    def delete(self, id):
        abort_if_company_not_found(id)
        session = db_session.create_session()
        regcompany = session.query(RegCompany).get(id)
        session.delete(regcompany)
        session.commit()
        return jsonify({'success': 'OK'})


    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('phone')
        parser.add_argument('location')
        parser.add_argument('INN')
        parser.add_argument('about')
        parser.add_argument('accepted')
        parser.add_argument('email')
        parser.add_argument('password')

        args = parser.parse_args()
        session = db_session.create_session()


        regcompany = session.query(RegCompany).get(id)
        if not regcompany:
            return abort(404, message=f"RegCompany not found")

        if args['name']: regcompany.name = args['name']
        if args['phone']: regcompany.phone = args['phone']
        if args['location']: regcompany.location = args['location']
        if args['INN']: regcompany.INN = args['INN']
        if args['about']: regcompany.about = args['about']
        if args['accepted']: regcompany.accepted = bool(args['accepted'])
        if args['email']: regcompany.email = args['email']
        if args['password']: regcompany.set_password(args['password'])

        session.commit()
        return jsonify({'success': 'OK'})



parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('location', required=True)
parser.add_argument('INN', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)




class RegCompanyListResource(Resource):
    def get(self):
        session = db_session.create_session()
        regcompany = session.query(RegCompany).all()
        return jsonify({'reg_company': [item.to_dict(
            only=('id', 'name', 'phone')) for item in regcompany]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        regcompany = RegCompany(
            name=args['name'],
            about=args['about'],
            phone=args['phone'],
            location=args['location'],
            INN=args['INN'],
            email=args['email']
        )
        regcompany.set_password(args['password'])

        session.add(regcompany)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_company_not_found(id):
    session = db_session.create_session()
    regcompany = session.query(RegCompany).get(id)
    if not regcompany:
        abort(404, message=f"RegCompany {id} not found")