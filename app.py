from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger
from flask_jwt_extended import  JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
#lembrar de trocar a senha no final
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:alfa@localhost:5432/prova'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'title': 'Api',
    'version': 1.0,

}

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ALGORITHM"] = "HS256"
app.config['JWT_BLACKLIST_ENABLED'] = True

jwt = JWTManager(app)

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message' : 'You have been logged out'}), 401
