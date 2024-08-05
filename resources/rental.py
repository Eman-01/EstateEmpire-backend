from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
from sqlalchemy import and_, not_

from models import db, Rental

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('image', type=str, required=True, help='Image is required')
parser.add_argument('description', type=str, required=True, help='Description is required')
parser.add_argument('location', type=str, required=True, help='Location is required')
parser.add_argument('price', type=int, required=True, help='Price isrequired')


class RentalResource(Resource):
    def get(self, id=None):
        if id:
            rental = Rental.query.filter_by(id=id).first()
            
            if rental:
                return rental.to_dict(), 200
            else:
                return {"message": "Property not found"}, 404
        
        else:
            rentals = [n.to_dict() for n in Rental.query.all() ]
            reponse = make_response(jsonify(rentals), 200)
            return reponse
        
    def patch(self, id=None):
        args = parser.parse_args()
        rental = Rental.query.filter_by(id = id).first()
        
        if rental == None:
            return {'message': "Property not found"}, 404
        
        rental.name = args['name']
        rental.image = args['image']
        rental.location = args['location']
        rental.description = args['description']
        rental.price = args['price']
        
        db.session.commit()
        return {"message": "Property updated successfully"}  
        
        
    def post(self):
        args = parser.parse_args()
        
        new_property = Rental(
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
        rental = Rental.query.get_or_404(id)
        db.session.delete(rental)
        db.session.commit()
        return {'message': "Property deleted"}, 200
            