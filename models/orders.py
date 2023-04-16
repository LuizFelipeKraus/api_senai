from app import db
from models.address import Address
from models.products import Products
from models.order_itens import OrderItem
import json

class Order(db.Model):
    """
        Order Model
        Class representing an order in the e-commerce application.

        Attributes:
            id (int): The ID of the order (primary key).
            user_id (int): The ID of the user who placed the order (foreign key).
            address_id (int): The ID of the shipping address (foreign key).
            status (str): The status of the order, one of 'Pendente', 'Pago', 'Enviado', 'Entregue', or 'Cancelado'.
            order_date (datetime): The date and time when the order was placed.

        Relationships:
            user (User): The user who placed the order (backref).
            address (Address): The shipping address (backref).

        Methods:
            find_orders(cls, order_id): Returns the order with the given ID, or None if it does not exist.
            save_orders(self): Saves the order to the database.
            update_orders(self, user_id, address_id, status, order_date): Updates the order with the given attributes.
            delete_orders(self): Deletes the order from the database.
            json(self): Returns a dictionary representation of the order.
            json_orders_user(cls, user_id): Returns a dictionary representation of all orders placed by the user with the given ID.

    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey(
        'addresses.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('Pendente', 'Pago', 'Enviado',
                       'Entregue', 'Cancelado', name='order_status'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)

    # Relacionamentos
    user = db.relationship('User', backref='orders')
    address = db.relationship('Address', backref='orders')

    def __init__(self, orders_id, user_id, address_id, status, order_date):
        self.id = orders_id
        self.user_id = user_id
        self.address_id = address_id
        self.status = status
        self.order_date = order_date

    def __repr__(self):
        return '<Orders %r>' % self.id

    def json(self):
        return {
            'user': self.user_id,
            'endereco': self.address_id,
            'status': self.status,
            'data': str(self.order_date),
        }

    @classmethod
    def find_orders(cls, order_id):
        order = cls.query.filter_by(id=order_id).first()
        if order:
            return order
        return None

    def save_orders(self):
        db.session.add(self)
        db.session.commit()

    def update_orders(self, user_id, address_id, status, order_date):
        self.user_id = user_id
        self.address_id = address_id
        self.status = status
        self.order_date = order_date

    def delete_orders(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def json_orders_user(cls, user_id, data_inicio = None, data_fim = None):
        order_list = []
        if data_inicio and data_fim:
            orders = cls.query.filter_by(user_id=user_id).filter(cls.order_date.between(data_inicio, data_fim)).all()
        else:
            orders = cls.query.filter_by(user_id=user_id).all()
        if orders:
            for order in orders:
                address = Address.query.filter_by(id=order.address_id).first()
                itens_produto = OrderItem.query.filter_by(order_id=order.id).all()
                produtos = [Products.query.filter_by(id=item_produto.product_id).first() for item_produto in itens_produto]

                valor_total = sum(item_produto.result for item_produto in itens_produto)

                order_dict = {
                    "id": order.id,
                    "status": order.status,
                    "data": str(order.order_date),
                    "produtos": [
                        {"nome": produto.name, "preco": float(item_produto.price), "quantidade": item_produto.quantity, "total": float(item_produto.result)}
                        for item_produto, produto in zip(itens_produto, produtos)
                    ],
                    "endereco": address.description + ',' + address.postal_code + ',' + address.city  + '-' + address.state,
                    "total_ordem" : float(valor_total)
                }
                order_dict["produtos"] = list(order_dict["produtos"])
                order_list.append(order_dict)
        return {"order": order_list}