from app import app
from db_config import db   
   
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
