from flask_restful import Resource, reqparse
from models.products import Products
from flask_jwt_extended import jwt_required


class AllProducts(Resource):
    @jwt_required()
    def get(self):
        return {'Products' : [products.json() for products in Products.query.all()]}


class ProductResource(Resource):
    """
    Attributes:
        argumentos (RequestParser): An instance of RequestParser class that defines the expected arguments for requests.

    Methods:
        get(product_id): Retrieves an product by its ID.
        post(product_id): Creates a new product.
        put(product_id): Updates an existing product.
        delete(product_id): Deletes an product by its ID.
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('name', type = str, required = True, help = "The field 'name' cannot be left blanck")
    argumentos.add_argument('description', type = str, help = "The field 'description' cannot be left blanck")
    argumentos.add_argument('price', type = float,required = True, help = "The field 'price' cannot be left blanck")

    @jwt_required()
    def get(self, product_id):
        product = Products.find_product(product_id)
        if product:
            return product.json(), 200

        return {'message' : 'product not found!'}, 404

    @jwt_required()
    def post(self, product_id):
        if Products.find_product(product_id):
            return {'message' : f'product id {product_id} already exists.'}, 400

        dados = ProductResource.argumentos.parse_args()

        product = Products(product_id, **dados)
        try:
            product.save_product()
        except:
            return {'message' : 'An internal error ocurred trying to save product.'}, 500
        return product.json()

    @jwt_required()
    def put(self, product_id):
        dados = ProductResource.argumentos.parse_args()

        product_encontrado = Products.find_product(product_id)

        if product_encontrado:
            product_encontrado.update_product(**dados)
            try:
                product_encontrado.save_product()
            except:
                return {'message' : 'An internal error ocurred trying to save product.'}, 500
            return product_encontrado.json(), 200

        product = Products(product_id, **dados)
        try:
            product.save_product()
        except:
            return {'message' : 'An internal error ocurred trying to save product.'}, 500
        return product.json(), 201

    @jwt_required()
    def delete(self, product_id):
        product = Products.find_product(product_id)
        if product:
            try:
                product.delete_product()
            except:
                return {'message' : 'An error ocurred trying to delete product.'}, 500
            return {'message' : 'product deleted.'}
        return {'message' : 'product not found.'}, 404
