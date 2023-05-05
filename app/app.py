from pathlib import Path
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from database.database import db
from database.models import User

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

@app.route("/createaccount", methods=["GET", "POST"])
def createaccount() -> str:
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
        if user.__auth__() == True:
            return 'Authentication successful', 200

        
    return render_template("admin.html")

@app.route("/admin/store", methods=["GET"])
def adminStore() -> str:
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



if __name__ == "__main__":
    app.run(debug=True)