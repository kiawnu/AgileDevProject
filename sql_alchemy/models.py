from database import db #this might need to come from a different script?

class UserAccount():
    user_id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String)
    email = db.Column(db.String)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.screen_name,
            "email":self.email,
        }

class Order():
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("useraccount.id"), primary_key=True)
    products = db.relationship("OrderLines", back_populates="order")

    def to_json(self):
        product_list = []
        price_list = []
        for product in self.products:
            product_list.append({"name":product.name, "quantity":product.quantity})
            price_list.append(product.product.price * product.quantity)

class OrderLines(): #should just have an order id and a product id, no name or line id required
    line_id = db.Column(db.Integer)
    name = db.Column(db.ForeignKey("product.name"))

class Product():
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def to_json(self):
        return {
            "id":self.product_id,
            "name":self.name,
            "price":self.price,
            "quantity":self.quantity,
        }