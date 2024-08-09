from sqlalchemy import MetaData, DateTime, func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Property(db.Model, SerializerMixin):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    units = db.Column(db.Integer)
    status = db.Column(db.String)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=func.now())
    
    unit_type = db.relationship('Unit_type', back_populates = 'unit_types')
    user = db.relationship('User', back_populates = 'users')
    serialize_only = ('id', 'name', 'image', 'location', 'description', 'price', 'units', 'type', 'status', 'unit_type_id','created_at')

class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    mpesa_code = db.Column(db.Integer)
    purchased_at = db.Column(db.DateTime, default=func.now())
    
    property = db.relationship('Property', back_populates = 'properties')
    
    serialize_only = ('id', 'amount', 'mpesa_code', 'purchased_at')
    
class Rented(db.Model, SerializerMixin):
     __tablename__ = "rented"
     
     id = db.Column(db.Integer, primary_key=True)
     unit_number = db.Column(db.Integer)
     status = db.Column(db.String)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
     property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
     rented_at = db.Column(db.DateTime, default=func.now())
    
     
    
class UnitType(db.Model, SerializerMixin):
    __tablename__ = 'unit_types'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    rentals = db.relationship('Rent', back_populates='unit_type')
    for_sales = db.relationship('For_Sale', back_populates='unit_type')
    
    serialize_only = ('id', 'name')

class Agent(db.Model, UserMixin):
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
   
    
    rentals = db.relationship('Rental', back_populates='agent', lazy=True)
    for_sales = db.relationship('For_Sale', back_populates='agent', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
        }
