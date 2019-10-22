import sqlite3
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse, request

from security import authenticate, identity


def get_by_name(name):
        conn   = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM items WHERE name=?"

        results = cursor.execute(query, (name,)) 
        
        row = results.fetchone()
        conn.close()

        if row:
            return {'item': {'name': row[0], 'price' :row[1]}}

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
        )

    
    @jwt_required()
    def get(self,name):

        item = get_by_name(name)
        if item:
            return item 
        return {'error' : 'item not found'}, 404

    def delete(self, name):

        item = get_by_name(name)

        if not item:
            return {'error' : 'item with that name does not exists'}
            
        else:
            conn  = sqlite3.connect('data.db')
            cursor = conn.cursor()
            query = "DELETE FROM items WHERE name=?"

            cursor.execute(query, (name,))
            conn.commit()
            conn.close()
            return {'message' : 'Item has been deleted'}               

      
        

    def put(self,name):
       pass
       return item       


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

        cursor.execute(query) 
        
        items = cursor.fetchall()
        conn.close()
        return items

    
    def post(self):
      
        data = Items.parser.parse_args()

        item = get_by_name(data['name'])

        if item:
            return {'error' : 'item with the same name already exists'}
            
        else:
            conn  = sqlite3.connect('data.db')
            cursor = conn.cursor()
            query = "INSERT INTO items VALUES(?,?)"

            cursor.execute(query, (data['name'],data['price']))
            conn.commit()
            conn.close()
            return data, 201                

