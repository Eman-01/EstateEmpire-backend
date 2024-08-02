from sqlalchemy import MetaData, DateTime, func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# Initialize metadata
metadata = MetaData(naming_convention = convention)


db = SQLAlchemy(metadata=metadata)

# Models

class Property(db.Model, SerializerMixin):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    image = db.Column(db.String)
    description = db.Column(db.String)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=func.now())
    
    rents = db.relationship('Rent', back_populates = 'property')
    purchases = db.relationship('Purchase', back_populates = 'property')
    
    serialize_only = ('id', 'name', 'description', 'status', 'created_at')
    
    
class Rent(db.Model, SerializerMixin):
    __tablename__ = 'rents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    created_at = db.Column(db.DateTime, default=func.now())
    
    user = db.relationship ('User', back_populates = 'rents')
    property = db.relationship('Property', back_populates = 'rents')
    
    serialize_only = ('id', 'user_id', 'property_id', 'created_At')
    
class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    created_at = db.Column(db.DateTime, default=func.now())
    
    user = db.relationship('User', back_populates='purchases')
    property = db.relationship('Property', back_populates='purchases')
    
    serialize_only = ('id', 'user_id', 'property_id', 'created_At')
    
class Agent(db.Model, SerializerMixin):
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    
    properties = db.relationship('Property', backref='agent', lazy=True)
    
    serialize_rules = ('-password',)
    
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    
    rents = db.relationship('Rent', back_populates='user')
    purchases = db.relationship('Purchase', back_populates='user')

    serialize_rules = ('-password',)
    
    