from pathlib import Path
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from database.database import db
from database.models import User, Product, Cache, Product, Order, OrderLine

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path(".").resolve()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        data = request.json
        username = data["username"]
        password = data["password"]

        user = User.query.filter_by(
            username=username, password=password).first()
        if not user:
            return 'Invalid login credentials', 401

        login_user(user)

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("home"))


@app.route("/createaccount", methods=["GET", "POST"])
def create_account():
    try:
        if request.method == "POST":
            data = request.json
            err_desc = ""

            if type(data["username"]) != type("e"):
                err_desc = "'username' must be a string."
                raise AttributeError

            if User.query.filter_by(username=data["username"]):
                err_desc = "'username' must be unique."
                raise AttributeError

            if type(data["password"]) != type("e"):
                err_desc = "'password' must be a string."
                raise AttributeError

            user = User(
                username=data["username"],
                password=data["password"]
            )

            db.session.add(user)
            db.session.commit()

            login_user(user)

            return (
                f"Account Created.",
                200
            )
        return render_template("createacc.html")

    except AttributeError:
        return (
            err_desc,
            400
        )


@app.route("/info")
def info() -> str:
    return render_template("infoFront.html")


@app.route("/info/<int:id>")
def infoID(id) -> str:
    return render_template("infoPlant.html")


@app.route("/checkout")
def checkout() -> str:
    return render_template("checkout.html")


@app.route("/store")
@login_required
def store() -> str:
    return render_template("storeFront.html")


@app.route("/api/product/<int:product_id>", methods=["GET"])
def retreive_product(product_id):
    try:
        prod = db.session.get(Product, product_id)
        return (
            prod.to_json(),
            200
        )
    except:
        return (
            f"Product #{product_id} could not be found.",
            404
        )


@app.route("/admin/store/<int:product_id>", methods=["DELETE"])
def remove_product(product_id):
    try:
        if current_user.__auth__() != True:
            raise PermissionError
        product = db.session.get(Product, product_id)
        db.session.delete(product)
        db.session.commit()
        return (
            f"Product #{product_id} removed successfully.",
            200
        )
    except PermissionError:
        return (
            f"err",
            401
        )
    except:
        return (
            f"Product #{product_id} could not be found.",
            404
        )


@app.route("/admin/store/newproduct", methods=["POST"])
def create_product():
    data = request.json
    try:
        if current_user.__auth__() != True:
            raise PermissionError

        err_list = []
        err_desc = ""

        if type(data["name"]) != type("e"):
            err_list.append("name must be string")
        if type(data["sname"]) != type("e"):
            err_list.append("scientific name must be string")
        if type(data["price"]) != type(0) and type(data["price"]) != type(0.0):
            err_list.append("price must be numeric")
        if type(data["quantity"]) != type(0):
            err_list.append("quantity must be an integer")

        if len(err_list) > 0:
            for item in err_list:
                err_desc += f"{item}"
                if item != err_list[-1]:
                    err_desc += ", "

    except AttributeError:
        return (
            f"Invalid format for product attributes: {err_desc}.",
            400
        )

    except PermissionError:
        return (
            f"You do not have permission to add a new product.",
            401
        )

    new_prod = Product(
        img=data.get("img"),
        name=data.get("name"),
        sname=data.get("sname"),
        price=round(float(data.get("price")), 2),
        quantity=data.get("quantity")
    )
    db.session.add(new_prod)
    db.session.commit()
    return (
        f"Product #{new_prod.id} added successfully.",
        200
    )

@app.route("/orders/process", methods=["GET"])
@login_required
def process_order():
    try:
        order = Order.query.filter_by(user_id=current_user.id).first()
        order_line = OrderLine.query.filter_by(order_id=order.id).all()
        
        for product in order_line:
            product_obj = db.session.get(OrderLine, (product.product_id, order.id))
            plant = db.session.get(Product, product.product_id)
            if (plant.quantity - product_obj.quantity) < 0:
                product_obj.quantity = plant.quantity
                plant.quantity = 0
            else:
                plant.quantity -= product_obj.quantity

            db.session.delete(product_obj)
            db.session.commit()
            
        db.session.query(OrderLine).filter(OrderLine.order.has(Order.user_id == current_user.id)).delete() 
        db.session.delete(order)
        db.session.commit()
        return 'Order Processed', 200
    except AttributeError:
        return "Please save cart before checking out", 400


@app.route("/admin/store/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    try:
        data = request.json

        try:
            if db.session.get(Product, product_id) == None:
                raise FileNotFoundError
            if current_user.__auth__() != True:
                raise PermissionError

            err_list = []
            err_desc = ""

            if type(data["name"]) != type("e") and type(data["name"]) != type(None):
                err_list.append("name must be string")
            if type(data["sname"]) != type("e") and type(data["sname"]) != type(None):
                err_list.append("sname must be string")
            if type(data["img"]) != type("e") and type(data["img"]) != type(None):
                err_list.append("img must be string")
            if type(data["price"]) != type(0) and type(data["price"]) != type(None) and type(data["price"]) != type(0.0):
                err_list.append("price must be numeric")
            if type(data["quantity"]) != type(0) and type(data["quantity"]) != type(None):
                err_list.append("quantity must be an integer")

            if len(err_list) > 0:
                for item in err_list:
                    err_desc += f"{item}"
                    if item != err_list[-1]:
                        err_desc += ", "

        except AttributeError:
            return (
                f"Invalid format for product attributes: {err_desc}.",
                400
            )

        old_prod = db.session.get(Product, product_id)

        # checks update values
        if data.get("name") == None:
            data.update({"name": old_prod.name})
        if data.get("sname") == None:
            data.update({"sname": old_prod.name})
        if data.get("img") == None:
            data.update({"img": old_prod.name})
        if data.get("price") == None:
            data.update({"price": old_prod.price})
        if data.get("quantity") == None:
            data.update({"quantity": old_prod.quantity})

        new_prod = Product(
            id=product_id,
            name=data.get("name"),
            sname=data.get("sname"),
            img=data.get("img"),
            price=round(float(data.get("price")), 2),
            quantity=data.get("quantity")
        )

        db.session.delete(old_prod)
        db.session.commit()
        db.session.add(new_prod)
        db.session.commit()
        return (
            f"Product #{product_id} updated successfully.\nOld Product: {old_prod.to_json()}\nNew Product: {new_prod.to_json()}",
            200
        )
    except FileNotFoundError:
        return (
            f"Product #{product_id} could not be found.",
            404
        )


@app.route("/admin", methods=["GET", "POST"])
def admin() -> str:
    if request.method == "POST":
        data = request.json
        username = data["username"]
        password = data["password"]

        user = User.query.filter_by(
            username=username, password=password).first()
        login_user(user)

        if not user:
            return 'Invalid login credentials', 401
        if user.__auth__():
            return 'Authentication successful', 200

    return render_template("admin.html")


@app.route("/admin/store", methods=["GET"])
def admin_store() -> str:
    try:
        user_id = f"{current_user}"
        user = User.query.filter_by(id=int(user_id)).first()
    except ValueError:
        return redirect(url_for("home"))

    if user.__auth__():
        return render_template("adminStore.html")
    return redirect(url_for("unauthorized"))


@app.route("/unauthorized", methods=["GET"])
def unauthorized():
    return render_template('unauthadmin.html')


@login_manager.unauthorized_handler
def login_redirect():
    return render_template('unauthuser.html')


@app.route("/admin/store/<string:name>", methods=["POST"])
def admin_add_item(name) -> str:
    """This function will add an item to the database

    Args:
        name (_type_): _description_

    Returns:
        str: _description_
    """
    # data = request.json #{'name': 'apple tree', 'price': 1, 'quantity': 1}

    # product = Product(name=data['name'], price=float(data['price']), quantity=int(data['quantity']))
    # item = Product.query.filter_by(name=data['name']).first()
    pass


@app.route("/api/products", methods=["GET"])
def get_products() -> str:
    products = Product.query.all()
    return jsonify([p.to_json() for p in products])


@app.route("/orders", methods=["GET"])
@login_required
def retrieve_orders():
    orders = current_user.orders
    return jsonify([o.to_json() for o in orders])


@app.route("/orders/<int:order_id>", methods=["GET"])
@login_required
def retrieve_order(order_id):
    try:
        orders = current_user.orders

        for order in orders:
            if order.id == order_id:
                return jsonify(order.to_json()), 200

        if db.session.get(Order, order_id) == None:
            raise FileNotFoundError
        else:
            raise PermissionError

    except FileNotFoundError:
        return (
            f"Order #{order_id} could not be found.",
            404
        )
    except PermissionError:
        return (
            # make this work with current unauthorized access code
            f"You do not have permission to view order #{order_id}.",
            401
        )


@app.route("/orders", methods=["POST"])
@login_required
def create_order():
    try:
        data = request.json
        message = "Order Created"
        if current_user.orders:
            order = Order.query.filter_by(user_id=current_user.id).first()
            db.session.query(OrderLine).filter(OrderLine.order.has(Order.user_id == current_user.id)).delete() 
            message = "Order Updated"
        else:
            order = Order(user_id=current_user.id)
            db.session.add(order)
            db.session.commit()

        for item in data["products"]:
            line = OrderLine(
                product_id=int(item["p_id"]),
                order_id=order.id,
                quantity=int(item["quantity"])
            )
            db.session.add(line)
            db.session.commit()
            
        return (
            f"{message}",
            200
        )
    except AttributeError:
        return (
            "Invalid attributes",
            400
        )


@app.route("/orders/<int:order_id>/<int:product_id>", methods=["DELETE"])
@login_required  # use request.json for the product to be removed, not the URL
def remove_order_line(order_id, product_id):
    try:
        order = db.session.get(Order, order_id)

        if order == None:
            err_desc = f"Order #{order_id} could not be found."
            raise FileNotFoundError
        if order.user_id != current_user.id:
            raise PermissionError

        for product in order.products:
            if product.product_id == product_id:
                db.session.delete(product)
                db.session.commit()
                return (
                    f"Product #{product_id} successfully removed from order #{order_id}.",
                    200
                )

        err_desc = f"Product #{product_id} could not be found in order #{order_id}."
        raise FileNotFoundError

    except FileNotFoundError:
        return (
            err_desc,
            404
        )

    except PermissionError:
        return (
            f"You do not have permission to delete order #{order_id}.",
            401
        )


@app.route("/orders/<int:order_id>", methods=["DELETE"])
@login_required
def remove_order(order_id):
    try:
        order = db.session.get(Order, order_id)
        if order == None:
            raise FileNotFoundError
        if order.user_id != current_user.id:
            raise PermissionError

        for line in order.products:
            db.session.delete(line)

        db.session.delete(order)
        db.session.commit()

        return (
            f"Order #{order_id} removed successfully.",
            200
        )

    except FileNotFoundError:
        return (
            f"Order #{order_id} could not be found.",
            404
        )

    except PermissionError:
        return (
            f"You do not have permission to delete order #{order_id}.",
            401
        )


@app.route("/orders/<int:order_id>", methods=["PUT"])
@login_required
def append_product(order_id):
    try:
        order = db.session.get(Order, order_id)
        data = request.json
        err_desc = ""

        if order == None:
            raise FileNotFoundError
        if order.user_id != current_user.id:
            raise PermissionError
        if type(data["products"]) != type([]):
            err_desc = "Invalid JSON format: 'products' must be List"
            raise AttributeError

        for product in data["products"]:
            if type(product) == type({}):
                if type(product["p_id"]) == type(0) and type(product["quantity"]) == type(0) and db.session.get(Product, product["p_id"]):
                    new_line = OrderLine(
                        product_id=product["p_id"],
                        order_id=order.id,
                        quantity=product["quantity"]
                    )
                    for item in order.products:
                        if item.product_id == new_line.product_id:
                            print(item)
                            db.session.delete(item)
                            db.session.commit()

                    order.products.append(new_line)
                    db.session.commit()

                else:
                    err_len = 0
                    err_desc = "Invalid JSON format: "
                    if type(product["p_id"]) != type(0) or not db.session.get(Product, product["p_id"]):
                        err_desc += "'p_id' must be a valid product id"
                        err_len = 1
                    if type(product["quantity"]) != type(0):
                        if err_len == 1:
                            err_desc += ", "
                        err_desc += "'quantity' must be an integer"
                    raise AttributeError
            else:
                err_desc = "Invalid JSON format: items in 'products' List must be Dict"
                raise AttributeError

        return (
            f"Products successfully appended to order #{order_id} successfully.",
            200
        )

    except FileNotFoundError:
        return (
            f"Order #{order_id} could not be found.",
            404
        )

    except PermissionError:
        return (
            f"You do not have permission to append to order #{order_id}.",
            401
        )

    except AttributeError:
        return (
            f"{err_desc}.",
            400
        )


@app.route("/store/<int:id>")
@login_required
def product_store(id) -> str:
    return render_template("storePlant.html")


@app.route("/cache/<string:get_url>", methods=["GET"])
def get_cache(get_url) -> str:
    try:
        content = Cache.query.filter_by(url=get_url).first()
        return jsonify(content.to_json())
    except:
        return f'', 400


@app.route("/cache/<string:get_url>", methods=["PUT"])
def put_cache(get_url) -> str:
    data = request.json
    cache = Cache(url=get_url, content=str(data))
    db.session.add(cache)
    db.session.commit()
    return 'Added to cache'


if __name__ == "__main__":
    app.run(debug=True)
