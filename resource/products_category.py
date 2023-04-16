from flask_restful import Resource, reqparse
from models.products_category import ProductCategory
from models.products import Products
from models.categories import Categories
from flask_jwt_extended import jwt_required


#class Allcategory(Resource):
#    #@jwt_required()
#    def get(self, product_id):
#product_category
#        return {'category' : [category.json() for category in Categories.query.all()]}


class ProductCategoryResource(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('product_id', type = int, required = True, help = "The field 'product_id' cannot be left blanck")
    argumentos.add_argument('category_id', type = int, required = True, help = "The field 'category_id' cannot be left blanck")


    #@jwt_required()
    def get(self, category_id, product_id):
        product_category = ProductCategory.find_product_category(category_id, product_id)
        if product_category:
            return product_category.json(), 200

        return {'message' : 'category not found!'}, 404

    #@jwt_required()
    def post(self, category_id, product_id):
        if ProductCategory.find_product_category(category_id, product_id):
            return {'message' : f'product-category id {category_id} already exists.'}, 400

        dados = ProductCategoryResource.argumentos.parse_args()

        product_category = ProductCategory(category_id, **dados)
        try:
            product_category.save_product_category()
        except:
            return {'message' : 'An internal error ocurred trying to save product-category.'}, 500
        return product_category.json()

    #@jwt_required()
    def put(self, category_id, product_id):
        dados = ProductCategoryResource.argumentos.parse_args()

        product_category_encontrado = ProductCategory.find_product_category(category_id, product_id)

        if product_category_encontrado:
            product_category_encontrado.update_product_category(**dados)
            try:
                product_category_encontrado.save_product_category()
            except:
                return {'message' : 'An internal error ocurred trying to save product-category.'}, 500
            return product_category_encontrado.json(), 200

        product_category = ProductCategory(category_id, **dados)
        try:
            product_category.save_product_category()
        except:
            return {'message' : 'An internal error ocurred trying to save product-category.'}, 500
        return product_category.json(), 201

    #@jwt_required()
    def delete(self, category_id, product_id):
        product_category = ProductCategory.find_product_category(category_id, product_id)
        if product_category:
            try:
                product_category.delete_product_category()
            except:
                return {'message' : 'An error ocurred trying to delete product-category.'}, 500
            return {'message' : 'product-category deleted.'}
        return {'message' : 'product-category not found.'}, 404
