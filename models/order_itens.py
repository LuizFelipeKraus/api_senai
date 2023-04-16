from app import db

class OrderItem(db.Model):
    """
        OrderItem Model
        A class used to represent an order item in the database.

        Attributes
        ----------
        id : int
            The unique identifier for the order item.
        order_id : int
            The ID of the order that this item belongs to.
        product_id : int
            The ID of the product associated with this item.
        price : decimal.Decimal
            The price of the item.
        quantity : int
            The quantity of the item.
        result : decimal.Decimal
            The total result of the item, calculated as price multiplied by quantity.

        Methods
        -------
        find_order_items(order_item_id)
            Find an order item by its ID.
        json()
            Return a dictionary representing the order item in JSON format.
        save_order_items()
            Save the order item to the database.
        update_order_items(order_item_id, order_id, product_id, price, quantity, result)
            Update the attributes of the order item.
        delete_order_items()
            Delete the order item from the database.
    """

    __tablename__ = 'orders_items'

    id = db.db.Column(db.Integer, primary_key=True)
    order_id = db.db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    price = db.db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.db.Column(db.Integer, nullable=False)
    result = db.db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', backref='items')
    product = db.relationship('Products', backref='orders')

    def __init__(self, order_item_id, order_id, product_id, price, quantity, result):
        self.id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.result = result



    def __repr__(self):
        return '%r' % self.id

    @classmethod
    def find_order_items(cls, order_item_id):
        order_item = cls.query.filter_by(id=order_item_id).first()
        if order_item:
            return order_item
        return None


    def json(self):
        return {
            'id' : self.id,
            'order_id' : self.order_id,
            'product_id' : self.product_id,
            'price' : float(self.price),
            'quantity' : self.quantity,
            'result' : float(self.result)
        }

    def save_order_items(self):
            db.session.add(self)
            db.session.commit()

    def update_order_items(self, order_item_id, order_id, product_id, price, quantity, result):
        self.id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.result = result


    def delete_order_items(self):
        db.session.delete(self)
        db.session.commit()