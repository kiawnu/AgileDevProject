"""
This is to create admin users :
    these users will be able to login and be able to change items in the database
    through api calls
"""


from app import app, db
from database.models import User

with app.app_context():
    obj = User(username='admin', password='password', auth=True)
    db.session.add(obj)
    obj = User(username='username', password='password')
    db.session.add(obj)
    print(f"Admin added\nUsername: admin\nPassword: password\n---\nRegular User added\nUsername: username\nPassword: password")
    db.session.commit()
