from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse, request

from security import authenticate, identity
from  models.item import ItemModel

class Item(Resource):
    
    @jwt_required()
    def get(self,name):

        item = ItemModel.get_by_name(self,name)
        if item:
            return item.json() , 200
        return {'error' : 'item not found'}, 404

    def delete(self, name):

        item = ItemModel.get_by_name(name)

        if not item:
            return {"error" : "item with the name '{}' does not exists".format(name)}, 404
            
        else:
            item.delete_from_db()
            return {'message' : 'Item has been deleted'} , 200                


class Items(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
        )

    parser.add_argument('name',
    type=str,
    required=True,
    help="This field cannot be left blank!"
        )

    parser.add_argument('store_id',
    type=int,
    required=True,
    help="Every Item requires a store id"
        )        

    def get(self):
        # return {'items': list(map(lambda x : x.json(), ItemModel.query.all()))}
        return {'items' : [x.json() for x in ItemModel.query.all()]}
        
    def post(self):
      
        data = Items.parser.parse_args()

        if ItemModel.get_by_name(data['name']):
            return {"error" : "item with the same name '{}' already exists".format(data['name'])}, 400
             
        # item = ItemModel(data['name'], data['price'],data['store_id'])           
        item = ItemModel(**data)           
        
        try:
            item.save_to_db()
        except:
            return {'error':'something weired happened while inserting data to db'}, 500

        return item.json(), 201                        

    def put(self):

        data = Items.parser.parse_args()

        item = ItemModel.get_by_name(data['name'])       

        if item is None:
            item = ItemModel(**data)
        else:
            item.name     = data['name']
            item.price    = data['price']
            item.store_id = data['store_id']

        return item.json()
