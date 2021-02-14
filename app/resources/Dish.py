from flask_restful import Resource
from sqlalchemy import exc
from flask import send_from_directory

from models.db import Dish, Ingredient, Foodstuff
from models.db import DCategory, DStage, DUnit, DPrePackType
from resources.schema.dish.request import DishRequestSchema

from app import db

from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs


class DishList(MethodResource, Resource):
    @doc(tags=['dish'], description='Read all dishes.')
    def get(self):
        '''
        Get method represents a GET API method
        '''
        dishes = Dish.query.order_by(Dish.id.desc()).all()
        results = [ob.as_json() for ob in dishes]
        return results, 200

    @doc(tags=['dish'], description='Create dish.')
    @use_kwargs(DishRequestSchema(), location=('json'))
    def post(self, **kwargs):
        validation_errors = DishRequestSchema().validate(kwargs)
        if Dish.query.filter(Dish.name == kwargs["name"]).first():
            validation_errors.update(
                {
                    'name': [
                        'Already exist'
                    ]
                }
            )
        if validation_errors:
            return {
                       'messages': validation_errors
                   }, 400

        dish = Dish()
        dish.name = kwargs['name']
        dish.description = kwargs['description']
        dish.portion = kwargs['portion']
        dish.cook_time = kwargs['cook_time']
        dish.all_time = kwargs['all_time']
        for category_id in kwargs['categories']:
            category = DCategory.query.get(category_id)
            if category:
                dish.categories.append(category)

        try:
            db.session.add(dish)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {
                       'messages': e.args
                   }, 503

        return dish.as_json(), 200


class DishDetail(MethodResource, Resource):
    @doc(tags=['dish'], description='Read dish.')
    def get(self, id):
        dish = Dish.query.filter(Dish.id == id).first_or_404()
        return dish.as_full_json(), 200

    @doc(tags=['dish'], description='Update dish.')
    @use_kwargs(DishRequestSchema(), location=('json'))
    def put(self, id, **kwargs):
        validation_errors = DishRequestSchema().validate(kwargs)
        if validation_errors:
            return {
                       'messages': validation_errors
                   }, 400

        dish = Dish.query.filter(Dish.id == id).first_or_404()
        dish.name = kwargs['name']
        dish.description = kwargs['description']
        dish.portion = kwargs['portion']
        dish.cook_time = kwargs['cook_time']
        dish.all_time = kwargs['all_time']

        new_category_list = []
        for category_id in kwargs['categories']:
            new_category_list.append(DCategory.query.get(category_id))
        dish.categories = new_category_list

        try:
            db.session.add(dish)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {
                       'messages': e.args
                   }, 503

        return dish.as_json(), 200

    @doc(tags=['dish'], description='Delete dish.')
    def delete(self, id):
        dish = Dish.query.filter(Dish.id == id).first_or_404()
        try:
            db.session.add(dish)
            db.session.delete(dish)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {
                       'messages': e.args
                   }, 503

        return '', 204


class DishImg(MethodResource, Resource):
    @doc(tags=['dish'], description='Read dish img.')
    def get(self, id):
        response = send_from_directory(directory='images/', filename='{}.jpg'.format(id))
        return response
