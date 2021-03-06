from flask import Flask
from flask_caching import Cache
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import Configuration
from flask_migrate import Migrate

from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
cache = Cache(app)
docs = FlaskApiSpec(app)

from resources.Dish import DishList, DishDetail, DishImg
from resources.Ingredient import IngredientList, IngredientDetail
from resources.Foodstuff import FoodstuffList, FoodstuffDetail
from resources.Dictionary import StoreSectionList, StoreSectionDetail, \
                                 UnitList, UnitDetail, \
                                 StageList, StageDetail,\
                                 CategoryList, CategoryDetail, \
                                 PrePackTypeList, PrePackTypeDetail
from resources.Menu import MenuList, MenuDetail
from resources.Menu import MenuDishList, MenuDishDetail
from resources.Menu import MenuShoppingList, MenuPrePackList

api.add_resource(DishList, '/dishes')
api.add_resource(DishDetail, '/dishes/<id>')
api.add_resource(DishImg, '/dishes/<dish_id>/img')
api.add_resource(IngredientList, '/dishes/<dish_id>/ingredients')
api.add_resource(IngredientDetail, '/dishes/<dish_id>/ingredients/<id>')

api.add_resource(FoodstuffList, '/foodstuffs')
api.add_resource(FoodstuffDetail, '/foodstuffs/<id>')

api.add_resource(StoreSectionList, '/store_sections')
api.add_resource(StoreSectionDetail, '/store_sections/<id>')
api.add_resource(UnitList, '/units')
api.add_resource(UnitDetail, '/units/<id>')
api.add_resource(StageList, '/stages')
api.add_resource(StageDetail, '/stages/<id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(CategoryDetail, '/categories/<id>')
api.add_resource(PrePackTypeList, '/pre_pack_types')
api.add_resource(PrePackTypeDetail, '/pre_pack_types/<id>')

api.add_resource(MenuList, '/menus')
api.add_resource(MenuDetail, '/menus/<id>')

api.add_resource(MenuDishList, '/menus/<menu_id>/dishes')
api.add_resource(MenuDishDetail, '/menus/<menu_id>/dishes/<id>')

api.add_resource(MenuShoppingList, '/menus/<menu_id>/shopping_list')
api.add_resource(MenuPrePackList, '/menus/<menu_id>/pre_pack_list')

docs.register(DishList)
docs.register(DishDetail)
docs.register(IngredientList)
docs.register(IngredientDetail)
docs.register(DishImg)

docs.register(FoodstuffList)
docs.register(FoodstuffDetail)

docs.register(StoreSectionList)
docs.register(StoreSectionDetail)
docs.register(UnitList)
docs.register(UnitDetail)
docs.register(StageList)
docs.register(StageDetail)
docs.register(CategoryList)
docs.register(CategoryDetail)
docs.register(PrePackTypeList)
docs.register(PrePackTypeDetail)

docs.register(MenuList)
docs.register(MenuDetail)
docs.register(MenuDishList)
docs.register(MenuDishDetail)

docs.register(MenuShoppingList)
docs.register(MenuPrePackList)
