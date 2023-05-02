from database import db #this might need to come from a different script?

order_product = db.Table("order_product",
                          db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
                          db.Column("product_id", db.Integer, db.ForeignKey("product.id"))
                          )

class UserAccount(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("useraccount.id"), primary_key=True)
    products = db.relationship("Product", secondary=order_product, backref="orders")

    def to_json(self):
        product_list = []
        price_list = []
        for product in self.products:
            product_list.append({"name":product.name, "quantity":product.quantity})
            price_list.append(product.product.price * product.quantity)
        
        return {
            "id":self.id,
            "user":self.user_id,
            "products":product_list,
            "price_total":round(sum(price_list), 2)
        }

class Product(db.Model):
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

# class OrderLines(db.Model): #should just have an order id and a product id, no name or line id required
#     product_id = db.Column(db.ForeignKey("product.id"))
#     order_id = db.Column(db.ForeignKey("order.id"))
    
#     product = db.relationship("Product")
#     order = db.relationship("Order")