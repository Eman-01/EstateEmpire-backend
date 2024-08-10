import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models import db
from resources.user import SignupResource, LoginResource
from resources.property import PropertyResource, PropertyForRentResource, PropertyForSaleResource
from resources.unit_type import UnitTypeResource

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"  
app.json.compact = False


CORS(app)


bcrypt = Bcrypt(app)


jwt = JWTManager(app)


migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>EstateEmpire</h1>"

api.add_resource(PropertyResource, '/properties', '/properties/<int:id>')
api.add_resource(PropertyForSaleResource, '/properties/for-sale', '//properties/for-sale/<int:id>')
api.add_resource(PropertyForRentResource, '/properties/for-rent', '/properties/for-rent//<int:id>')
api.add_resource(UnitTypeResource, '/unit_types', '/unit_types/<int:id>')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
