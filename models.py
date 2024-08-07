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

class Rental(db.Model, SerializerMixin):
    __tablename__ = 'rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    status = db.Column(db.String)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    created_at = db.Column(db.DateTime, default=func.now())

    agent = db.relationship('Agent', back_populates='rentals')
    serialize_only = ('id', 'name', 'image', 'location', 'description', 'price', 'status', 'created_at')

class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=func.now())
    
    agent = db.relationship('Agent', back_populates='purchases')
    serialize_only = ('id', 'name', 'image', 'location', 'description', 'price', 'status', 'created_at')

class Agent(db.Model, UserMixin):
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
   
    
    rentals = db.relationship('Rental', back_populates='agent', lazy=True)
    purchases = db.relationship('Purchase', back_populates='agent', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
        }
