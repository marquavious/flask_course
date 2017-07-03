# Import dependencies
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# Adds our diffrent models and resources to our
# Application. They are needed here so the tables can be
# Created by create_tables on initial load
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

# Lets Flask know that the dadabase will be in the root directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Turns off traking for SQL modifications because
# Flasks does that for us already
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Not entirely sure why we set a key
app.secret_key = '1234'

# Lets Api know that the application is a
# rest api
api = Api(app)

# Runs this before the first api hit
# To make sure all the tables are made in the
# sql database
@app.before_first_request
def create_tables():
    db.create_all()

# Sets up jet authentication
jwt = JWT(app,authenticate,identity)

# Adds routes to hit
# Maps "Resource" items to endpoints
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# Lets server know this is the main file to run
if __name__ == '__main__':
    # imports our data base from out db file
    # initiates it
    from db import db
    db.init_app(app)

    # Runs out application on route 5000
    # Debug is on to see print statements ect.
    app.run(port=5000, debug=True)
