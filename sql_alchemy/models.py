from database import db

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    orders = db.relationship("Order", backref="user_account")

    is_admin = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "admin":self.is_admin,
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_account.id"))
    
    products = db.relationship("OrderLine", back_populates="order")

    def to_json(self):
        product_list = []
        price_list = []
        for product in self.products:
            product_list.append({"name":db.session.get(Product, product.product_id).name, "quantity":product.quantity})
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
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "price":self.price,
            "quantity":self.quantity,
        }

class OrderLine(db.Model):
    product_id = db.Column(db.ForeignKey("product.id"), primary_key=True)
    order_id = db.Column(db.ForeignKey("order.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product")
    order = db.relationship("Order", back_populates="products")