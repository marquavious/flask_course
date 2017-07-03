# Import dependencies
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# Subclasses Resource to communicate with the api cleanly
class Item(Resource):

    # Creating a parser to get required parameters on the api hit
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help="Every item needs a store id"
    )

    # I took of JWT to avoid be authenticated every hit
    # This makes it required to be authenticated in order
    # To hit this endpoint
    # @jwt_required()
    def get(self,name):

        # Uses ItemModel to communicate with out database
        item = ItemModel.find_by_name(name)
        if item:
            return item.json
        # else
        return{'message':'Item not found'}

    def post(self,name):

        # If there is a item by that name already
        if ItemModel.find_by_name(name):
            return {'message':"An item with the name '{}' already exists".format(name)}, 400

        # Get data from the parser
        data = Item.parser.parse_args()

        # Create a ItemModel wit the data grabbed
        item = ItemModel(name,**data)

        # Try saving to the database
        try:
            item.save_to_db()
        except:
            return {'message':"An error occured inserting item."}, 500

        # Return json of the item to show it was created
        return item.json(), 201


    def delete(self,name):

        # Find Item
        item = ItemModel.find_by_name(name)

        # If the item exists
        if item:
            item.delete_from_db()

        return {'message':'Item has been deleted'}

    def put(self,name):

        # Grab data from parser
        data = Item.parser.parse_args()

        # Look for an item
        item = ItemModel.find_by_name(name)

        # If the item doesnt exists, create one
        if item is None:
            item = ItemModel(name,**data)
        # Else just update price
        else:
            item.price = data['price']

        # Save it or update it to the DB
        item.save_to_db()

        # Return json of the item to show it was created
        return item.json()

# Class of Item list
class ItemList(Resource):

    # Returns all items in the DB in a json format
    def get(self):
        return {'items':[x.json() for x in ItemModel.query.all()]}
        # return {'items':list(map(lambda x: x.json(), ItemModel.query.all())}
