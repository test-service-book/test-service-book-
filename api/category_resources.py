from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.category import Category


class CategoryResource(Resource):
    def get(self, id):
        abort_if_category_not_found(id)
        session = db_session.create_session()
        category = session.query(Category).get(id)
        return jsonify({'category': category.to_dict(
            only=('id', 'name'), )})

    def delete(self, id):
        abort_if_category_not_found(id)
        session = db_session.create_session()
        category = session.query(Category).get(id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name')


        args = parser.parse_args()
        session = db_session.create_session()

        category = session.query(Category).get(id)
        if not category:
            return abort(404, message=f"Category not found")

        if args['name']: category.name = args['name']

        session.commit()
        return jsonify({'success': 'OK'})



parser = reqparse.RequestParser()
parser.add_argument('name', required=True)


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        category = session.query(Category).all()
        return jsonify({'category': [item.to_dict(
            only=('id', 'name')) for item in category]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category(
            name=args['name']
        )
        session.add(category)
        session.commit()
        return jsonify({'success': 'OK'})



def abort_if_category_not_found(id):
    session = db_session.create_session()
    category = session.query(Category).get(id)
    if not category:
        abort(404, message=f"Category {id} not found")