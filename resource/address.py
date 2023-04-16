from flask_restful import Resource, reqparse
from models.address import Address
from flask_jwt_extended import jwt_required, get_jwt_identity


class AllAddress(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return {'address' : [address.json() for address in Address.query.filter_by(user_id = user_id).all()]}



class AddressResource(Resource):
    """
    Attributes:
        argumentos (RequestParser): An instance of RequestParser class that defines the expected arguments for requests.

    Methods:
        get(address_id): Retrieves an address by its ID.
        post(address_id): Creates a new address.
        put(address_id): Updates an existing address.
        delete(address_id): Deletes an address by its ID.
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('user_id', type = str, required = True, help = "The field 'user_id' cannot be left blanck")
    argumentos.add_argument('description', type = str, help = "The field 'description' cannot be left blanck")
    argumentos.add_argument('postal_code', type = str,required = True, help = "The field 'postal_code' cannot be left blanck")
    argumentos.add_argument('street', type = str, help = "The field 'street' cannot be left blanck")
    argumentos.add_argument('complement', type = str,required = True, help = "The field 'complement' cannot be left blanck")
    argumentos.add_argument('neighborhood', type = str, required = True, help = "The field 'neighborhood' cannot be left blanck")
    argumentos.add_argument('city', type = str,required = True, help = "The field 'city' cannot be left blanck")
    argumentos.add_argument('state', type = str, required = True, help = "The field 'state' cannot be left blanck")

    @jwt_required()
    def get(self, address_id):
        address = Address.find_address(address_id)
        if address:
            return address.json(), 200

        return {'message' : 'address not found!'}, 404

    @jwt_required()
    def post(self, address_id):
        if Address.find_address(address_id):
            return {'message' : f'address id {address_id} already exists.'}, 400

        dados = AddressResource.argumentos.parse_args()

        print(dados)

        address = Address(address_id, **dados)
        try:
            address.save_address()
        except:
            return {'message' : 'An internal error ocurred trying to save address.'}, 500
        return address.json()

    @jwt_required()
    def put(self, address_id):
        dados = AddressResource.argumentos.parse_args()

        address_encontrado = Address.find_address(address_id)

        if address_encontrado:
            address_encontrado.update_address(**dados)
            try:
                address_encontrado.save_address()
            except:
                return {'message' : 'An internal error ocurred trying to save address.'}, 500
            return address_encontrado.json(), 200

        address = Address(address_id, **dados)
        try:
            address.save_address()
        except:
            return {'message' : 'An internal error ocurred trying to save address.'}, 500
        return address.json(), 201

    @jwt_required()
    def delete(self, address_id):
        address = Address.find_address(address_id)
        if address:
            try:
                address.delete_address()
            except :
                return {'message' : 'An error ocurred trying to delete address.'}, 500
            return {'message' : 'address deleted.'}
        return {'message' : 'address not found.'}, 404
