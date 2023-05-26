from database.database import db
from flask_login import UserMixin
from flask import jsonify

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String)
    orders = db.relationship("Order", backref="user")
    auth = db.Column(db.Boolean, default=False)
    
    
    def __repr__(self):
        return f"{self.id}"
    
    def get_id(self):
        return self.id
    
    def __auth__(self):
        return self.auth
    
    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "admin":self.auth,
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),  autoincrement=False)
    completed = db.Column(db.Boolean, default=False)
    
    products = db.relationship("OrderLine", back_populates="order")

    def to_json(self):
        product_list = []
        price_list = []
        for product in self.products:
            p = db.session.get(Product, product.product_id)
            product_list.append({"img":p.img, "p_id":p.id, "plantName":p.name, "price":f"CA$ {p.price}", "quantity":product.quantity, "sname":p.sname})
            price_list.append(db.session.get(Product, product.product_id).price * product.quantity)
        
        return {
            "id":self.id,
            "user":self.user_id,
            "products":product_list,
            "price_total":round(sum(price_list), 2)
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sname = db.Column(db.String)
    img = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "sname":self.sname,
            "price":self.price,
            "img": self.img,
            "quantity":self.quantity,
        }

class OrderLine(db.Model):
    product_id = db.Column(db.ForeignKey("product.id"), primary_key=True)
    order_id = db.Column(db.ForeignKey("order.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product")
    order = db.relationship("Order", back_populates="products")

class Cache(db.Model):
    url = db.Column(db.String, primary_key=True)
    content = db.Column(db.String)
    
    def to_json(self):
        return self.content