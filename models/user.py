from db_config import db

class UserModel(db.Model):
    __tablename__ = 'users'
     
    # id_ = db.Column(db.models.IntegerField(_("")))
    id_ = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()       

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id_= id_).first() 