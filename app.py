import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models import db
from resources.agent import SignupResource, LoginResource

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this to a secure key
app.json.compact = False

# Setup CORS
CORS(app)

# Setup bcrypt
bcrypt = Bcrypt(app)

# Setup JWT
jwt = JWTManager(app)

# Setup database and migrations
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>EstateEmpire</h1>"

# Add API resources
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
