from pathlib import Path
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from database.database import db
from database.models import User, Product, Cache, Product

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
        
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return 'Invalid login credentials', 401

        login_user(user)

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("home"))

@app.route("/info")
def info() -> str:
    return render_template("infoFront.html")


@app.route("/info/<int:id>")
def infoID(id) -> str:
    return render_template("infoPlant.html")

@app.route("/createaccount", methods=["GET", "POST"])
def create_account() -> str:
    if request.method == "POST":
        data = request.json
        username = data["username"]
        password = data["password"]

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return f"Account Created", 200

    return render_template("createacc.html")


@app.route("/store")
@login_required
def store() -> str:
    return render_template("storeFront.html")

@app.route("/api/product/<int:product_id>", methods=["GET"])
def retrive_product(product_id):
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

@app.route("/store/<int:product_id>", methods=["DELETE"])
def remove_item(product_id):
    try:
        product = db.session.get(Product, product_id)
        db.session.delete(product)
        db.session.commit()
        return (
            f"Product #{product_id} removed successfully.",
            200
        )
    except:
        return (
            f"Product #{product_id} could not be found.",
            404
        )

@app.route("/store/newproduct", methods=["POST"])
def create_product():
    try:
        data = request.json
        new_prod = Product(
            name=data.get("name"),
            price=data.get("price"),
            quantity=data.get("quantity")
            )
        db.session.add(new_prod)
        db.session.commit()
        return (
            f"Product #{new_prod.id} added successfully.",
            200
        )
        
    except:
        return (
            "err num",
            "err msg"
        )

@app.route("/store/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        data = request.json

        try:
            if db.session.get(Product, product_id) == None:
                raise LookupError
            
            err_list = []
            
            if type(data.get("name")) is not type("e") or type(None):
                err_list.append("name must be string")
            if type(data.get("price")) is not type(0.0) or type(None) or type(0):
                err_list.append("price must be numeric")
            if type(data.get("quantity")) is not type(0) or type(None):
                err_list.append("quantity must be an integer")
            
            if len(err_list) > 0:
                raise ValueError

        except LookupError:
            return (
                f"Product #{product_id} could not be found.",
                404
            )
        
        except ValueError:
            return (
                f"Invalid format for update attributes: {err_list}"
            )
        
        old_prod = db.session.get(Product, product_id)

        #checks update values
        if data.get("name") == None:
            data.update({"name":old_prod.name})
        if data.get("price") == None:
            data.update({"price":old_prod.price})
        if data.get("quantity") == None:
            data.update({"quantity":old_prod.quantity})

        new_prod = Product(
            id=product_id,
            name=data.get("name"),
            price=data.get("price"),
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
    except:
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

        user = User.query.filter_by(username=username, password=password).first()
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
    
    if user.__auth__() == True: 
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