from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User
from resources.otp_validation import OtpValidation

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
        otp = OtpValidation().generate_otp()
        new_user = User(email=email, contact=contact, password_hash=hashed_password, role=role, email_verified=False, otp=otp)
        
        db.session.add(new_user)
        db.session.commit()

        # Send OTP to user's email
        OtpValidation().send_otp(email, otp)

        return {"message": "User created successfully. Please verify your email."}, 201

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

        if not user.email_verified:
            return {"message": "Please verify your email before logging in."}, 403

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token, "user": user.to_dict()}, 200

class EmailVerificationResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        input_otp = data.get('otp')

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User not found."}, 404

        if user.otp == input_otp:
            user.email_verified = True
            user.otp = None  # Clear the OTP after verification
            db.session.commit()
            return {"message": "Email verified successfully."}, 200
        else:
            return {"message": "Invalid OTP."}, 400