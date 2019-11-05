import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.users  import UserRegister
from resources.items  import Item,Items
from resources.stores import Store, Stores

# created an object of flask using a unique name
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']       = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS']          = True # To allow flask to propagate exception even if debug is set to false on app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'minkowski'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Items ,'/items')        
api.add_resource(Item ,'/items/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(UserRegister, '/register')        

if __name__ == '__main__':
    from db_config import db #To prevent circular import
    db.init_app(app)
    app.run(debug=True)
