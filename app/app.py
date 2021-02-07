from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config.from_object(Configuration)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

from resources.Recipe import RecipeDetail, RecipeImg, RecipeList
from resources.Recipe import RecipeIngredientList, RecipeIngredientDetail
from resources.Ingredient import IngredientList, IngredientDetail
from resources.Ingredient import StoreSectionList, StoreSectionDetail
from resources.Menu import MenuList, MenuDetail
from resources.Menu import MenuDishList, MenuDishDetail

api.add_resource(RecipeList, '/recipe')
api.add_resource(RecipeDetail, '/recipe/<id>')
api.add_resource(RecipeImg, '/recipe/<id>/img')
api.add_resource(RecipeIngredientList, '/recipe/<recipe_id>/ingredient')
api.add_resource(RecipeIngredientDetail, '/recipe/<recipe_id>/ingredient/<id>')

api.add_resource(IngredientList, '/ingredient')
api.add_resource(IngredientDetail, '/ingredient/<id>')

api.add_resource(StoreSectionList, '/store_section')
api.add_resource(StoreSectionDetail, '/store_section/<id>')

api.add_resource(MenuList, '/menu')
api.add_resource(MenuDetail, '/menu/<id>')

api.add_resource(MenuDishList, '/menu/<menu_id>/dish')
api.add_resource(MenuDishDetail, '/menu/<menu_id>/dish/<id>')

docs.register(RecipeList)
docs.register(RecipeDetail)
docs.register(RecipeIngredientList)
docs.register(RecipeIngredientDetail)
docs.register(RecipeImg)

docs.register(IngredientList)
docs.register(IngredientDetail)
docs.register(StoreSectionList)
docs.register(StoreSectionDetail)

docs.register(MenuList)
docs.register(MenuDetail)
docs.register(MenuDishList)
docs.register(MenuDishDetail)
