from app import db

class ProductCategory(db.Model):
    __tablename__ = 'products_categories'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)


    def __init__(self, product_id, category_id):
            self.product_id = product_id
            self.category_id = category_id

    def json(self):
        return {
            'product_id' : self.product_id,
            'category_id' : self.category_id 
        }

    @classmethod
    def find_product_category(cls, product_id, category_id):
        address = cls.query.filter_by(category_id = category_id, product_id = product_id).first()
        if address:
            return address
        return None

    def save_product_category(self):
            db.session.add(self)
            db.session.commit()

    def update_address(self,  product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id


    def delete_product_category(self):
        db.session.delete(self)
        db.session.commit()