from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User

class SignupResource(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')
        role = data.get('role')

        if not email or not contact or not password or not role:
            return {"message": "Missing required fields."}, 400

        if User.query.filter_by(email=email).first() or User.query.filter_by(contact=contact).first():
            return {"message": "User with this email or contact already exists."}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, contact=contact, password_hash=hashed_password, role=role)

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
    
    def get(self):
        users = User.query.all()
        if not users:
            return {"message": "No users found."}, 404

        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "email": user.email,
                "contact": user.contact,
                "role": user.role
            })

        return {"users": users_data}, 200

class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {"message": "Missing email or password."}, 400

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {"message": "Incorrect email or password."}, 401

        access_token = create_access_token(identity=user.id)

        return {"access_token": access_token, "user": user.to_dict()}, 200
