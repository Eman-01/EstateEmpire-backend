from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
from sqlalchemy import and_, not_

from models import db, Purchase
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('image', type=str, required=True, help='Image is required')
parser.add_argument('description', type=str, required=True, help='Description is required')
parser.add_argument('location', type=str, required=True, help='Location is required')
parser.add_argument('price', type=int, required=True, help='Price i srequired')


class PurchaseResource(Resource):
    def get(self, id=None):
        if id:
            purchase = Purchase.query.filter_by(id=id).first()
            
            if purchase:
                return purchase.to_dict(), 200
            else:
                return {"message": "purchase not found"}, 404
        
        else:
            purchase = [n.to_dict() for n in Purchase.query.all() ]
            reponse = make_response(jsonify(purchase), 200)
            return reponse
    def patch(self, id=None):
        args = self.parser.parser_args()
        purchase = Purchase.query.filter_by(id = id).first()
        
        if purchase == None:
            return {'message': "Property not found"}, 404
        
        purchase.name = args['name']
        purchase.image = args['image']
        purchase.location = args['loaction']
        purchase.description = args['description']
        purchase.price = args['price']
        
        db.session.commit()
        return {"message": "Property updated successfully"}
    
    def post(self):
        args = parser.parse_args()
        
        new_property = Purchase(
            name = args["name"],
            image = args["image"],
            location = args['location'],
            description = args["description"],
            price = args["price"]
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        return {"message" : "Property created successfully"}, 201
            
            
    def delete(self, id):
        purchase = Purchase.query.get_or_404(id)
        db.session.delete(purchase)
        db.session.commit()
        return {'message': "Property deleted"}, 200