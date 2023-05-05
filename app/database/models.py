from database.database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    auth = db.Column(db.Boolean, default=False)
    
    
    def __repr__(self):
        return f"{self.id}"
    def get_id(self):
        return self.id
    def __auth__(self):
        return self.auth