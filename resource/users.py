from flask_restful import Resource, reqparse
from app import api, swagger, app, jwt
from flask import request
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token
from blacklist import BLACKLIST

"""This module implements the RESTful API for user registration, login, and logout.

Classes:
- AllUsers: A Flask RESTful resource for getting all registered users.
- UserRegister: A Flask RESTful resource for registering a new user.
- UserLogin: A Flask RESTful resource for user login.
- UserLogout: A Flask RESTful resource for user logout.

Functions:
- None

Endpoints:
- /users: [GET] Returns a list of all registered users.
- /register: [POST] Registers a new user.
- /login: [POST] Logs in a user and returns an access token.
- /logout: [POST] Logs out a user and revokes the access token.

"""


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return {'Users' : [user.json() for user in User.query.all()]}


class UserRegister(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('email', type = str, required = True, help = "The field 'email' cannot be left blanck")
    atributos.add_argument('name', type = str, required = True, help = "The field 'name' cannot be left blanck")
    atributos.add_argument('password_hash', type = str, required = True, help = "The field 'senha' cannot be left blanck")

    def post(self):
        dados = UserRegister.atributos.parse_args()
        if User.find_by_login(dados['email']):
            return {'message' : f"The email {dados['email']} already exists."}
        password_hash  = generate_password_hash(dados['password_hash'])
        dados['password_hash'] = password_hash
        user = User(**dados)
        user.save_user()
        return {'message' : 'User created successfully!'}, 201

class UserLogin(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('email', type = str, required = True, help = "The field 'email' cannot be left blanck")
    atributos.add_argument('password_hash', type = str, required = True, help = "The field 'senha' cannot be left blanck")
    @classmethod
    def post(cls):
        dados = UserLogin.atributos.parse_args()

        user = User.find_by_login(dados['email'])

        if user  and check_password_hash(user.password_hash , dados['password_hash']):
            token_de_acesso = create_access_token(identity = user.id)
            return {'access_token' : token_de_acesso}, 200
        return {'message' : 'The username or password is incorrect.'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id =jwt.get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message' : 'Logged out successfully!'}, 200