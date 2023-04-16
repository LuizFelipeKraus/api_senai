from app import db

class Categories(db.Model):
    """
        Categories Model
        Represents a category in the application.

        Attributes:
            id (int): The unique identifier of the category.
            name (str): The name of the category.

        Methods:
            find_category(category_id): Returns the category with the given ID if it exists, otherwise None.
            save_category(): Persists the current category in the database.
            update_category(name): Updates the name of the current category with the given one.
            delete_category(): Deletes the current category from the database.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),  nullable=False)

    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name


    def __repr__(self):
        return '<Categories %r>' % self.name

    def json(self):
        return {
            'id' : self.id,
            'name' : self.name
        }

    @classmethod
    def find_category(cls, category_id):
        categories = cls.query.filter_by(id = category_id).first()
        if categories:
            return categories
        return None

    def save_category(self):
            db.session.add(self)
            db.session.commit()

    def update_category(self, name):
        self.name = name


    def delete_category(self):
        db.session.delete(self)
        db.session.commit()