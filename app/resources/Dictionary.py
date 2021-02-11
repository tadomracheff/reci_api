from flask_restful import Resource
from sqlalchemy import exc
from models.db import Foodstuff, DStoreSection, Ingredient
from resources.schema.dictionary.store_section.request import StoreSectionRequestSchema
from app import db

from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs


class StoreSectionList(MethodResource, Resource):
    @doc(tags=['dictionary'], description='Read store sections.')
    def get(self):
        r = DStoreSection.query.order_by(DStoreSection.id.desc()).all()
        results = [ob.as_json() for ob in r]
        return results, 200

    @doc(tags=['dictionary'], description='Create store section.')
    @use_kwargs(StoreSectionRequestSchema(), location=('json'))
    def post(self, **kwargs):
        validation_errors = StoreSectionRequestSchema().validate(kwargs)
        if validation_errors:
            return {
                       'messages': validation_errors
                   }, 400

        section = DStoreSection()
        section.name = kwargs['name']
        db.session.add(section)
        db.session.commit()
        return section.as_json(), 201


class StoreSectionDetail(MethodResource, Resource):
    @doc(tags=['dictionary'], description='Read store section.')
    def get(self, id):
        r = DStoreSection.query.filter(DStoreSection.id == id).first_or_404()
        return r.as_json(), 200

    @doc(tags=['dictionary'], description='Update store section.')
    @use_kwargs(StoreSectionRequestSchema(), location=('json'))
    def put(self, id, **kwargs):
        validation_errors = StoreSectionRequestSchema().validate(kwargs)
        if validation_errors:
            return {
                       'messages': validation_errors
                   }, 400
        section = DStoreSection.query.filter(DStoreSection.id == id).first_or_404()
        section.name = kwargs['name']

        try:
            db.session.add(section)
            db.session.commit()
            return section.as_json(), 200
        except exc.SQLAlchemyError as e:
            return {
                       'messages': e.args
                   }, 503

    @doc(tags=['dictionary'], description='Delete store section.')
    def delete(self, id):
        r = DStoreSection.query.filter(DStoreSection.id == id).first_or_404()

        foodstuffs = Foodstuff.query.filter(Foodstuff.store_section_id == id).all()
        if foodstuffs:
            return {
                       "message": "store section already use"
                   }, 422

        try:
            db.session.add(r)
            db.session.delete(r)
            db.session.commit()
            return '', 204
        except exc.SQLAlchemyError as e:
            return {
                       'messages': e.args
                   }, 503
