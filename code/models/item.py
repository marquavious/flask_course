# Import our database referance
from db import db

# Create a class of ItemModel that subclasses
# a SQLAlchemy model to be saved easily
class ItemModel(db.Model):

    # Lets the DB know that this class would be under
    # a row of items in the.
    __tablename__ = 'items'

    # These is the initilizers for the DB Model
    # Notice how they line up with our class properties
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))

    # This lets us talk and relate our StoreModel
    # ForeignKey does alot of things; binds the two elements together
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # Sets up a relationship to the StoreModel
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # Return a json version of itself
    def json(self):
        return {'name':self.name, 'price':self.price}

    # Find and return an item object
    # We can use query because its a SQLAlchemy model
    @classmethod
    def find_by_name(cls,name):
        # Finds and returns the first instance of a found object
        return cls.query.filter_by(name=name).first()

    # Save item to the database
    # We can use slef because its a SQLAlchemy model
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Delete item from database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
