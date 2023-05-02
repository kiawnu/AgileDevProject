from pathlib import Path
import datetime
from flask import Flask, jsonify, render_template, request


app = Flask(__name__, static_url_path='/static')
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = Path(".").resolve()
# db.init_app(app)


@app.route("/")
def home() -> str:
    return render_template("web/index.html")


if __name__ == "__main__":
    app.run(debug=True)