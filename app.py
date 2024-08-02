import os
from models import db
from flask_migrate import Migrate
from flask import FLask
from flask_restful import Resource, Api
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = FLask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Setup CORS
CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>EstateEmpire</h1>"