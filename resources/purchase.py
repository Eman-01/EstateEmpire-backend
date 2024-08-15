from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from models import db, Purchase


parser = reqparse.RequestParser()
parser.add_argument('amount', type=int, required=True)
parser.add_argument('user_id', type=int, required=True)
parser.add_argument('property_id', type=int, required=True)
parser.add_argument('mpesa_code', type=str, required=True)

class PurchaseResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        
        # Check if the user is requesting all purchases
        if request.args.get('all') == 'true' and current_user.is_admin:
            purchases = Purchase.query.all()
        else:
            purchases = Purchase.query.filter_by(user_id=current_user_id).all()
        
        return [purchase.to_dict() for purchase in purchases], 200

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        current_user_id = get_jwt_identity()
        
        if current_user_id != args['user_id']:
            return {"message": "Unauthorized"}, 403

        new_purchase = Purchase(
            amount=args['amount'],
            user_id=current_user_id,
            property_id=args['property_id'],
            mpesa_code=args['mpesa_code']
        )

        db.session.add(new_purchase)
        db.session.commit()

        return new_purchase.to_dict(), 201

class AllPurchasesResource(Resource):
    @jwt_required()
    def get(self):
        if not current_user.is_admin:
            return {"message": "Unauthorized"}, 403
        
        purchases = Purchase.query.all()
        return [purchase.to_dict() for purchase in purchases], 200