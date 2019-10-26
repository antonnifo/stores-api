import sqlite3
from db_config import db

class UserModel(db.Model):
    __tablename__ = 'users'
     
    # id_ = db.Column(db.models.IntegerField(_("")))
    id_ = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

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