from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from models import db, Rented

parser = reqparse.RequestParser()
parser.add_argument('unit_number', type=int, required=True)
parser.add_argument('user_id', type=int, required=True)
parser.add_argument('property_id', type=int, required=True)
parser.add_argument('mpesa_code', type=str, required=True)

class RentalResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        
        if request.args.get('all') == 'true' and current_user.is_admin:
            rented_units = self.get_all_rentals()
        else:
            rented_units = Rented.query.filter_by(user_id=current_user_id).all()
        
        return [rented_unit.to_dict() for rented_unit in rented_units], 200

    def get_all_rentals(self):
        if not current_user.is_admin:
            return {"message": "Unauthorized"}, 403
        return Rented.query.all()

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        current_user_id = get_jwt_identity()
        
        if current_user_id != args['user_id']:
            return {"message": "Unauthorized"}, 403
        
        existing_rental = Rented.query.filter_by(property_id=args['property_id'], user_id=current_user_id).first()
        if existing_rental:
            return {"message": "Rental already exists"}, 400

        new_rental = Rented(
            amount=args['amount'],
            user_id=current_user_id,
            property_id=args['property_id'],
            mpesa_code=args['mpesa_code']
        )

        db.session.add(new_rental)
        db.session.commit()

        return new_rental.to_dict(), 201
