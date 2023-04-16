from flask_restful import Resource, reqparse
from models.order_itens import OrderItem
from models.products import Products
from models.orders import Order
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime


class AllOrderItem(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {"orders": Order.json_orders_user(user_id)}


class OrderItemResource(Resource):
    """
    Attributes:
        argumentos (RequestParser): An instance of RequestParser class that defines the expected arguments for requests.

    Methods:
        multiply_quantity_price(quantity, price) : Return multiply values.
        get(order_item_id): Retrieves an OrderItem by its ID.
        post(order_item_id): Creates a new OrderItem.
        put(order_item_id): Updates an existing OrderItem.
        delete(order_item_id): Deletes an OrderItem by its ID.
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('order_id', type=int, required=True,
                            help="The field 'order_id' cannot be left blanck")
    argumentos.add_argument('product_id', type=int,
                            help="The field 'product_id' cannot be left blanck")
    argumentos.add_argument('quantity', type=int, required=True,
                            help="The field 'quantity' cannot be left blanck")

    def multiply_quantity_price(quantity, price):
        if quantity > 0:
            result = quantity * price
            return result

    @jwt_required()
    def get(self, order_item_id):
        order_item = OrderItem.find_order_items(order_item_id)
        if order_item:
            return order_item.json(), 200

        return {'message': 'order_item not found!'}, 404

    @jwt_required()
    def post(self, order_item_id):
        if OrderItem.find_order_items(order_item_id):
            return {'message': f'order_item id {order_item_id} already exists.'}, 400

        dados = OrderItemResource.argumentos.parse_args()
        price_product = Products.checks_products(dados['product_id'])

        if price_product:
            result = OrderItemResource.multiply_quantity_price(
                dados['quantity'], price_product)
            if result:
                dados['result'] = result
                dados['price'] = price_product
                order_item = OrderItem(order_item_id, **dados)
            else:
                return {'message': f'result must be greater than zero'}, 400
        else:
            return {'message': f'product not exists'}, 400
        try:
            order_item.save_order_items()
        except:
            return {'message': 'An internal error ocurred trying to save order_item.'}, 500
        return order_item.json()

    @jwt_required()
    def put(self, order_item_id):
        dados = OrderItemResource.argumentos.parse_args()

        order_item_encontrado = OrderItem.find_order_items(order_item_id)

        if order_item_encontrado:
            price_product = Products.checks_products(dados['product_id'])

            if price_product:
                result = OrderItemResource.multiply_quantity_price(
                    dados['quantity'], price_product)
                if result:
                    dados['result'] = result
                    dados['price'] = price_product
                    order_item = OrderItem(order_item_id, **dados)
                    order_item_encontrado.update_order_items(
                        order_item_id, **dados)
                else:
                    return {'message': f'result must be greater than zero'}, 400
            else:
                return {'message': f'product not exists'}, 400
            try:
                order_item_encontrado.save_order_items()
            except:
                return {'message': 'An internal error ocurred trying to save order_item.'}, 500
            return order_item_encontrado.json(), 200

        price_product = Products.checks_products(dados['product_id'])

        if price_product:
            result = OrderItemResource.multiply_quantity_price(
                dados['quantity'], price_product)
            if result:
                dados['result'] = result
                dados['price'] = price_product
                order_item = OrderItem(order_item_id, **dados)
            else:
                return {'message': f'result must be greater than zero'}, 400
        else:
            return {'message': f'product not exists'}, 400

        try:
            order_item.save_order_items()
        except:
            return {'message': 'An internal error ocurred trying to save order_item.'}, 500
        return order_item.json(), 201

    @jwt_required()
    def delete(self, order_item_id):
        order_item = OrderItem.find_order_items(order_item_id)
        if order_item:
            try:
                order_item.delete_order_items()
            except:
                return {'message': 'An error ocurred trying to delete order_item.'}, 500
            return {'message': 'order_item deleted.'}
        return {'message': 'order_item not found.'}, 404
