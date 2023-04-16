from flask_restful import Resource, reqparse
from models.categories import Categories
from flask_jwt_extended import jwt_required


class Allcategory(Resource):
    @jwt_required()
    def get(self):
        return {'category' : [category.json() for category in Categories.query.all()]}


class CategoryResource(Resource):
    """
    Attributes:
        argumentos (RequestParser): An instance of RequestParser class that defines the expected arguments for requests.

    Methods:
        get(category_id): Retrieves an category by its ID.
        post(category_id): Creates a new category.
        put(category_id): Updates an existing category.
        delete(category_id): Deletes an category by its ID.
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('name', type = str, required = True, help = "The field 'name' cannot be left blanck")


    @jwt_required()
    def get(self, category_id):
        category = Categories.find_category(category_id)
        if category:
            return category.json(), 200

        return {'message' : 'category not found!'}, 404

    @jwt_required()
    def post(self, category_id):
        if Categories.find_category(category_id):
            return {'message' : f'category id {category_id} already exists.'}, 400

        dados = CategoryResource.argumentos.parse_args()

        category = Categories(category_id, **dados)
        try:
            category.save_category()
        except:
            return {'message' : 'An internal error ocurred trying to save category.'}, 500
        return category.json()

    @jwt_required()
    def put(self, category_id):
        dados = CategoryResource.argumentos.parse_args()

        category_encontrado = Categories.find_category(category_id)

        if category_encontrado:
            category_encontrado.update_category(**dados)
            try:
                category_encontrado.save_category()
            except:
                return {'message' : 'An internal error ocurred trying to save category.'}, 500
            return category_encontrado.json(), 200

        category = Categories(category_id, **dados)
        try:
            category.save_category()
        except:
            return {'message' : 'An internal error ocurred trying to save category.'}, 500
        return category.json(), 201

    @jwt_required()
    def delete(self, category_id):
        category = Categories.find_category(category_id)
        if category:
            try:
                category.delete_category()
            except:
                return {'message' : 'An error ocurred trying to delete category.'}, 500
            return {'message' : 'category deleted.'}
        return {'message' : 'category not found.'}, 404
