import sqlite3 
from  db_config import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id_   = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2)) 
    
    def __init__(self,name,price):
        self.name  = name
        self.price = price

    def json(self):
        return {'name':name, 'price':price}

    def get_by_name(self,name):
        conn   = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM items WHERE name=?"

        results = cursor.execute(query, (name,)) 

        row = results.fetchone()
        conn.close()

        if row:
            return {'item': {'name': row[0], 'price' :row[1]}}


    def insert_data(self, data):
        conn  = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "INSERT INTO items VALUES(?,?)"

        cursor.execute(query, (data['name'],data['price']))
        conn.commit()
        conn.close()
                    