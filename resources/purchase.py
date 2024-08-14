from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Purchase, Property
from resources.mpesa import Mpesa

class PurchaseResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('property_id', type=int, required=True, help="Property ID cannot be blank")
    parser.add_argument('amount', type=int, required=True, help="Amount cannot be blank")
    parser.add_argument('phone_number', type=str, required=True, help="Phone number cannot be blank")
    
    @jwt_required()
    def post(self):
        data = PurchaseResource.parser.parse_args()
        current_user_id = get_jwt_identity()
        
        # Check if the property exists
        property = Property.query.filter_by(id=data['property_id'], status='available').first()
        if not property:
            return {"message": "Property not found or is not available"}, 404

        # Initiate M-Pesa payment
        mpesa = Mpesa()
        mpesa_response = mpesa.stk_push(phone_number=data['phone_number'], amount=data['amount'], transaction_desc=f"Purchase of {property.name}")

        if mpesa_response.get('error'):
            return {"message": "Payment initiation failed", "details": mpesa_response}, 400

        # Create the purchase record
        purchase = Purchase(
            amount=data['amount'],
            user_id=current_user_id,
            property_id=data['property_id'],
            mpesa_code=mpesa_response.get('CheckoutRequestID')  # Assuming CheckoutRequestID is returned
        )
        db.session.add(purchase)
        db.session.commit()

        # Update the property status
        property.status = 'sold'
        db.session.commit()

        return {"message": "Purchase successful", "purchase": purchase.to_dict()}, 201