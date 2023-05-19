"""
This is to create admin users :
    these users will be able to login and be able to change items in the database
    through api calls
"""

import csv
from app import app, db
from database.models import User, Product

with app.app_context():
    obj = User(username='admin', email='admin@website.com', password='password', auth=True)
    db.session.add(obj)
    obj = User(username='username', email='user@website.com', password='password')
    db.session.add(obj)
    print(f"Admin added\nUsername: admin\nPassword: password\n---\nRegular User added\nUsername: username\nPassword: password")
    db.session.commit()

data = []
with open("app/store.csv", "r") as fp:
        reader = csv.DictReader(fp)
        for line in reader:
            data.append(line)

with app.app_context():
    for item in data:
        item = Product(name = item['name'], sname = item['sname'], img = item['img'], price = item['price'], quantity = item['quantity'])
        db.session.add(item)
        print('*', end=' ')
    db.session.commit()
