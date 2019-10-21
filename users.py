import sqlite3
from flask_restful import Resource, reqparse

class User(object):

    def __init__(self, id_, username, password):
        self.id       = id_
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):

        conn   = sqlite3.connect('data.db')
        cursor = conn.cursor()

        q = "SELECT * FROM  users WHERE username=?"
        
        results = cursor.execute(q,(username,))
        row     = results.fetchone()
        
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()

        return user

    @classmethod
    def find_by_id(cls, id_):

        conn   = sqlite3.connect('data.db')
        cursor = conn.cursor()

        q = "SELECT * FROM  users WHERE id=?"
        
        results = cursor.execute(q,(id_,))
        row     = results.fetchone()
        
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()

        return user

class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201       