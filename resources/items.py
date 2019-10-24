import sqlite3
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse, request

from security import authenticate, identity
from  models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
        )

    
    @jwt_required()
    def get(self,name):

        item = ItemModel.get_by_name(self,name)
        if item:
            return item , 200
        return {'error' : 'item not found'}, 404

    def delete(self, name):

        item = ItemModel.get_by_name(self,name)

        if not item:
            return {'error' : 'item with that name does not exists'}, 400
            
        else:
            conn  = sqlite3.connect('data.db')
            cursor = conn.cursor()
            query = "DELETE FROM items WHERE name=?"

            cursor.execute(query, (name,))
            conn.commit()
            conn.close()
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

    def get(self):
        conn   = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM items"

        rows = cursor.execute(query) 
        # items = cursor.fetchall()
             
        items = []
        for row in rows:
            items.append({'name': row[0], 'price':row[1]})

        conn.close()    
        return {'items': items}, 200
    
    def post(self):
      
        data = Items.parser.parse_args()

        item = ItemModel.get_by_name(self,data['name'])

        if item:
            return {'error' : 'item with the same name already exists'}, 400
            
        else:
            ItemModel.insert_data(self,data)
            return data, 201                

    def put(self):

        data = Items.parser.parse_args()

        item = ItemModel.get_by_name(self,data['name'])       

        if item:
            conn  = sqlite3.connect('data.db')
            cursor = conn.cursor()
            query = "UPDATE items SET name=?,price=? WHERE name=?"

            cursor.execute(query, (data['name'],data['price'],data['name']))
            conn.commit()
            conn.close()
            return {'message' : 'Item has been updated'}                     
         
        else:
            
            ItemModel.insert_data(data)
            return data, 201 
