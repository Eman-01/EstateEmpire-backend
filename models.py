from enum import Enum
from sqlalchemy import MetaData, DateTime, func, Enum
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

class PropertyType(Enum):
    FOR_SALE = 'for_sale'
    FOR_RENT = 'for_rent'
    
class PropertyStatus(Enum):
    AVAILABLE = 'available'
    SOLD = 'sold'
    RENTED = 'rented'
    
class Property(db.Model, SerializerMixin):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    location = db.Column(db.String)
    type = db.Column(Enum(PropertyType.FOR_SALE, PropertyType.FOR_RENT, native_enum=False))
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    units = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    amenities = db.Column(db.String)
    status = db.Column(Enum(PropertyStatus.AVAILABLE, PropertyStatus.SOLD, PropertyStatus.RENTED, native_enum=False))
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=func.now())
    
    unit_type = db.relationship('UnitType', back_populates='properties')
    user = db.relationship('User', back_populates='properties')
    purchase = db.relationship('Purchase', back_populates='property', uselist=False, cascade="all, delete-orphan")
    rented = db.relationship('Rented', back_populates='property', cascade="all, delete-orphan")
    
    serialize_only = ('id', 'name', 'image', 'location', 'description', 'price', 'units', 'bedrooms', 'bathrooms', 'amenities', 'type', 'status', 'unit_type_id', 'user_id', 'created_at')

    def __repr__(self):
        return f'<Property {self.name}>'
    
class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    mpesa_code = db.Column(db.String)
    purchased_at = db.Column(db.DateTime, default=func.now())
    
    property = db.relationship('Property', back_populates='purchase', uselist=False)
    user = db.relationship('User', back_populates= 'purchases')
    
    serialize_only = ('id', 'amount', 'mpesa_code', 'purchased_at', 'user_id', 'property_id')
# Keeps track of the properties that have been rented   
class Rented(db.Model, SerializerMixin):
    __tablename__ = "rented"
    
    id = db.Column(db.Integer, primary_key=True)
    unit_number = db.Column(db.Integer)
    status = db.Column(db.String)
    amount = db.Column(db.Integer)
    mpesa_code = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    rented_at = db.Column(db.DateTime, default=func.now())
    
    serialize_only= ('id', 'unit_number', 'status', 'rented_at', 'user_id', 'property_id')
    user = db.relationship('User', back_populates='rented')
    property = db.relationship('Property', back_populates='rented')
    rental_payments = db.relationship('RentalPayments', back_populates='rented')
    
# keeps track of the rental payments
class RentalPayments(db.Model, SerializerMixin):
    __tablename__ = 'rental_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    rented_id = db.Column(db.Integer, db.ForeignKey('rented.id'))
    month = db.Column(db.String)
    mpesa_code = db.Column(db.String)
    status = db.Column(db.String)
    payment_date = db.Column(db.DateTime, default=func.now())
    
    rented = db.relationship('Rented', back_populates = 'rental_payments')
    
    serialize_only =('id', 'rented_id', 'month', 'mpesa_code', 'status', 'payment_date')
    
class UnitType(db.Model, SerializerMixin):
    __tablename__ = 'unit_types'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    properties = db.relationship('Property', back_populates='unit_type')
    
    serialize_only = ('id', 'name')

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(6), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())

    properties = db.relationship('Property', back_populates='user', lazy=True)
    rented = db.relationship('Rented', back_populates='user', lazy=True)
    purchases = db.relationship('Purchase', back_populates='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role
        }

