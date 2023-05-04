from models import User
import sys
sys.path.append("..")
from app import app, db

with app.app_context():
    obj = User(email='mafonso4@my.bcit.ca', pwd='password')
    db.session.add(obj)
    print(".", end="")
    print()
    db.session.commit()