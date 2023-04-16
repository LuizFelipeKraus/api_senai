from app import db

class Products(db.Model):
    """
        Products Model
        Represents a product in the store's inventory.

        Args:
            product_id (int): The unique identifier for the product.
            name (str): The name of the product.
            description (str): The description of the product.
            price (float): The price of the product.

        Attributes:
            id (int): The unique identifier for the product.
            name (str): The name of the product.
            description (str): The description of the product.
            price (float): The price of the product.

        Methods:
            json(): Returns a dictionary representation of the product.
            find_product(product_id: int) -> Optional[Products]: Finds a product by its unique identifier.
            checks_products(product_id: int) -> Optional[float]: Checks the price of a product by its unique identifier.
            save_product(): Saves the current product to the database.
            update_product(name: str, description: str, price: float): Updates the name, description, and price of the current product.
            delete_product(): Deletes the current product from the database.

    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),  nullable=False)
    description  = db.Column(db.Text)
    price  = db.Column(db.Numeric(10,2), nullable=False)

    def __init__(self, product_id, name, description, price):
        self.id = product_id
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Products %r>' % self.name

    def json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'price' : float(self.price)
        }

    @classmethod
    def find_product(cls, product_id):
        products = cls.query.filter_by(id = product_id).first()
        if products:
            return products
        return None

    def checks_products(product_id):
        address = Products.query.filter_by(id=product_id).first()

        if address:
            return address.price
        return None

    def save_product(self):
            db.session.add(self)
            db.session.commit()

    def update_product(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def delete_product(self):
        db.session.delete(self)
        db.session.commit()