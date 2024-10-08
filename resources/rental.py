from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from sqlalchemy.orm import joinedload
from models import db, Rented, Property
from resources.mpesa import Mpesa

class RentalResource(Resource):
    
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            
            # Query purchases for the current user, including related property information
            rentals = Rented.query.options(
                joinedload(Rented.property)
            ).filter_by(user_id=current_user_id).all()
            
            # Format the response data
            rent_data = []
            for rental in rentals:
                rent_data.append({
                    'id': rental.id,
                    'amount': rental.amount,
                    'rented_at': rental.rented_at.isoformat(),
                    'property': {
                        'name': rental.property.name,
                        'location': rental.property.location,
                        'price': rental.property.price
                    }
                })
            
            return {"purchases": rent_data}, 200

        except Exception as e:
            print("Error in RentalResource GET:", str(e))
            return {"message": "An error occurred while fetching rentals"}, 500
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            data = request.get_json()
            print("Received data:", data)

            property_id = data.get('property_id')
            amount = data.get('amount')
            phone_number = data.get('phone_number')

            if not all([property_id, amount, phone_number]):
                return {"message": "Missing required fields"}, 400

            property = Property.query.get(property_id)
            if not property:
                return {"message": "Property not found"}, 404

            mpesa = Mpesa()
            mpesa_response = mpesa.stk_push(
                phone_number=phone_number,
                amount=amount,
                transaction_desc=f"Purchase of property {property_id}"
            )

            print("Mpesa response:", mpesa_response)

            if 'error' in mpesa_response:
                return {"message": "Payment initiation failed", "details": mpesa_response}, 400

            # Create a new rental record
            rental = Rented(
                user_id=current_user,
                property_id=property_id,
                amount=amount,
                mpesa_code=mpesa_response.get('CheckoutRequestID')
            )
            db.session.add(rental)
            db.session.commit()

            return {"message": "Purchase initiated successfully", "details": mpesa_response}, 200

        except Exception as e:
            print("Error in PurchaseResource:", str(e))
            db.session.rollback()
            return {"message": str(e)}, 500