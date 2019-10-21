from flask import Flask
from  flask_restful import Api, Resource,request,reqparse



# created an object of flask using a unique name
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jos'
api = Api(app)


items = []

class Item(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )
    
    def get(self,name):
        
        item = next(filter(lambda x: x['name'] == name, items), None)

        return {'item': item}, 200 if item else 404       

    def delete(self, name):

        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
        

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

        if next(filter(lambda data: data['name'] == items[0]['name'], items), None):
            return {"message" : "item with  the name '{}' already exists".format(items[0]['name'])}, 400

        item = {
             'name'  : data['name'],
             'price' : data['price']
         } 

        items.append(item)
        return data, 201


               


api.add_resource(Items ,'/items')        
api.add_resource(Item ,'/items/<string:name>')        

if __name__ == '__main__':
    app.run(debug=True) )