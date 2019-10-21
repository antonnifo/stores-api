import sqlite3
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse, request

from security import authenticate, identity


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
        )
    
    @jwt_required()
    def get(self,name):
           
            conn   = sqlite3.connect('data.db')
            cursor = conn.cursor()

            query = "SELECT * FROM items WHERE name=?"

            results = cursor.execute(query, (name,)) 
           
            row = results.fetchone()
            conn.close()

            if row:
               return {'item': {'name': row[0], 'price' :row[1]}}
            return {'error' : 'item not found'}, 404   




    def delete(self, name):
      pass
        

    def put(self,name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item       


class Items(Resource):

     def get(self):

         if items:
             return items
         else:
             return  {'items' : None}, 404    

     def post(self):
         
        data = request.get_json()

        # if next(filter(lambda data: data['name'] == items[0]['name'], items), None):
        #     return {"message" : "item with  the name '{}' already exists".format(items[0]['name'])}, 400

        item = {
             'name'  : data['name'],
             'price' : data['price']
         } 

        items.append(item)
        return data, 201
