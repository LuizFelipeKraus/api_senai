from app import db

class User(db.Model):
    """
        User Model
        Class that represents a user in the system.

        Attributes:
            id (int): User's unique identifier.
            name(str): Username.
            email(str): User's email address.
            password_hash(str): User password hash.

        Methods:
            find_by_login(login: str) -> User:
                Searches for a user by email address.
            find_user(user_id: int) -> User:
                Searches for a user by unique identifier.
            save_user():
                Save the user to the database.
            json() -> dict:
                Returns a dictionary with user information.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def find_by_login(cls, login):
        usuario = cls.query.filter_by(email = login).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_user(cls, user_id):
        usuario = cls.query.filter_by(id = user_id).first()
        if usuario:
            return usuario
        return None

    def __repr__(self):
        return '<User %r>' % self.name

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'user_id' : self.id,
            'email' : self.email
        }
