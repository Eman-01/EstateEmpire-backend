from flask_restful import Resource, reqparse
from flask import jsonify, request
from sqlalchemy import and_
from models import db, RentalPayments, Rented
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument('rented_id', type=int, required=True, help='Rented ID is required')
parser.add_argument('month', type=str, required=True, help='Month is required')
parser.add_argument('mpesa_code', type=str, required=True, help='M-Pesa code is required')
parser.add_argument('status', type=str, required=True, help='Status is required')

class RentalPaymentsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = request.args.get('user_id')
        if user_id:
            # Fetch payments for a specific user
            payments = RentalPayments.query.join(Rented).filter(Rented.user_id == user_id).all()
        else:
            # Fetch all payments
            payments = RentalPayments.query.all()
        
        return jsonify([payment.to_dict() for payment in payments])

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        new_payment = RentalPayments(
            rented_id=args['rented_id'],
            month=args['month'],
            mpesa_code=args['mpesa_code'],
            status=args['status']
        )
        db.session.add(new_payment)
        db.session.commit()
        return new_payment.to_dict(), 201

class UserRentalPaymentsResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        payments = RentalPayments.query.join(Rented).filter(Rented.user_id == current_user_id).all()
        return jsonify([payment.to_dict() for payment in payments])