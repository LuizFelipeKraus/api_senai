from app import db

class Address(db.Model):
    """
        Address Model

        Represents an address for a user in the application.

        Attributes:
        -----------
        id : int
            The address unique identifier.
        user_id : int
            The user's unique identifier to which the address is associated.
        description : str
            A description to help identify the address (e.g. 'home', 'work', etc.).
        postal_code : str
            The postal code of the address.
        street : str
            The name of the street of the address.
        complement : str
            Additional information about the address (e.g. apartment number, floor, etc.).
        neighborhood : str
            The neighborhood of the address.
        city : str
            The city of the address.
        state : str
            The state of the address.

        Methods:
        --------
        find_address(cls, address_id):
            Returns an address by its unique identifier.
        user_address(cls, user_id):
            Returns all addresses associated with a user.
        save_address(self):
            Persists a new address in the database.
        update_address(self, user_id, description, postal_code, street, complement, neighborhood, city, state):
            Updates an existing address in the database.
        delete_address(self):
            Removes an address from the database.
    """
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    complement = db.Column(db.String(255))
    neighborhood = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), nullable=False)


    def __init__(self, address_id, user_id, description, postal_code, street, complement, neighborhood, city, state):
        self.id = address_id
        self.user_id = user_id
        self.description = description
        self.postal_code = postal_code[:9]
        self.street = street
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state



    def __repr__(self):
        return '%r' % self.id

    def json(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'description' : self.description,
            'postal_code' : self.postal_code,
            'street' : self.street,
            'complement' : self.complement,
            'neighborhood' : self.neighborhood,
            'city' : self.city,
            'state' : self.state,

        }

    @classmethod
    def find_address(cls, address_id):
        address = cls.query.filter_by(id = address_id).first()
        if address:
            return address
        return None

    @classmethod
    def user_address(cls, address_id):
        address = cls.query.filter_by(id = address_id)
        if address:
            return address
        return None

    def save_address(self):
            db.session.add(self)
            db.session.commit()

    def update_address(self,  user_id, description, postal_code, street, complement, neighborhood, city, state):
        self.user_id = user_id
        self.description = description
        self.postal_code = postal_code[:9]
        self.street = street
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state


    def delete_address(self):
        db.session.delete(self)
        db.session.commit()