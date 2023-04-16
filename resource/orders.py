from flask_restful import Resource, reqparse
from models.orders import Order
from models.address import Address
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime


class AllOrder(Resource):
    # @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {'Orders': [orderss.json() for orderss in Order.query.filter_by(user_id=user_id).all()]}


class OrderResource(Resource):
    """
    Attributes:
        argumentos (RequestParser): An instance of RequestParser class that defines the expected arguments for requests.

    Methods:
        checks_address(address): checks if the address exists for that user.
        get(order_id): Retrieves an order by its ID.
        post(order_id): Creates a new order.
        put(order_id): Updates an existing order.
        delete(order_id): Deletes an order by its ID.
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('user_id', type=int, required=True,
                            help="The field 'user_id' cannot be left blanck")
    argumentos.add_argument('address_id', type=int,
                            help="The field 'address_id' cannot be left blanck")
    argumentos.add_argument('status', type=str, required=True,
                            help="The field 'status' cannot be left blanck")

    def checks_address(address):
        user_id = get_jwt_identity()

        address = Address.query.filter_by(id=address, user_id=user_id).first()

        if address:
            return address.id
        return None

    @jwt_required()
    def get(self, orders_id):
        orders = Order.find_orders(orders_id)
        if orders:
            return orders.json(), 200

        return {'message': 'orders not found!'}, 404

    @jwt_required()
    def post(self, orders_id):
        if Order.find_orders(orders_id):
            return {'message': f'orders id {orders_id} already exists.'}, 400

        dados = OrderResource.argumentos.parse_args()

        address = OrderResource.checks_address(dados['address_id'])

        if address != dados['address_id']:
            return {'message': 'You are not authorized to create an order for this address.'}, 403

        dados['order_date'] = datetime.datetime.now().isoformat()
        orders = Order(orders_id, **dados)
        try:
            orders.save_orders()
        except:
            return {'message': 'An internal error ocurred trying to save orders.'}, 500
        return orders.json()

    @jwt_required()
    def put(self, orders_id):
        dados = OrderResource.argumentos.parse_args()

        orders_encontrado = Order.find_orders(orders_id)

        if orders_encontrado:
            address = OrderResource.checks_address(dados['address_id'])
            if address != dados['address_id']:
                return {'message': 'You are not authorized to create an order for this address.'}, 403

            dados['order_date'] = datetime.datetime.now().isoformat()
            orders_encontrado.update_orders(**dados)

            try:
                orders_encontrado.save_orders()
            except:
                return {'message': 'An internal error ocurred trying to save orders.'}, 500
            return orders_encontrado.json(), 200

        address = OrderResource.checks_address(dados['address_id'])
        if address != dados['address_id']:
            return {'message': 'You are not authorized to create an order for this address.'}, 403

        dados['order_date'] = datetime.datetime.now().isoformat()
        orders = Order(orders_id, **dados)

        try:
            orders.save_orders()
        except:
            return {'message': 'An internal error ocurred trying to save orders.'}, 500
        return orders.json(), 201

    @jwt_required()
    def delete(self, orders_id):
        orders = Order.find_orders(orders_id)
        if orders:
            try:
                orders.delete_orders()
            except:
                return {'message': 'An error ocurred trying to delete orders.'}, 500
            return {'message': 'orders deleted.'}
        return {'message': 'orders not found.'}, 404
