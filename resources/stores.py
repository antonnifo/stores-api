
from flask_restful import Resource, reqparse
from  models.store import StoreModel

class Store(Resource):
    
  
    def get(self,name):

        store = StoreModel.get_by_name(name)
        if store:
            return store.json() , 200
        return {'error' : 'store not found'}, 404

    def delete(self, name):

        store = StoreModel.get_by_name(name)

        if not store:
            return {"error" : "store with the name '{}' does not exists".format(name)}, 404
            
        else:
            store.delete_from_db()
            return {'message' : 'store has been deleted'} , 200                


class Stores(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('name',
    type=str,
    required=True,
    help="This field cannot be left blank!"
        )      

    def get(self):
        # return {'items': list(map(lambda x : x.json(), StoreModel.query.all()))}
        return {'soress' : [x.json() for x in StoreModel.query.all()]}
        
    def post(self):
      
        data = Stores.parser.parse_args()

        if StoreModel.get_by_name(data['name']):
            return {"error" : "store with the same name '{}' already exists".format(data['name'])}, 400
         
        store = StoreModel(data['name'])           
        
        try:
            store.save_to_db()
        except:
            return {'error':'something weired happened while inserting data to db'}, 500

        return store.json(), 201                        

