from pathlib import Path
import datetime
from flask import Flask, jsonify, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from database.database import db
from database.models import User

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path(".").resolve()
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home() -> str:
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        remember = request.form.get("remember")
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user, remember=remember)
            return redirect('/')
        else:
            return f"Invalid email or password.", 400

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("home"))

@app.route("/info")
@login_required
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


if __name__ == "__main__":
    app.run(debug=True)