from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
from sqlalchemy import and_, not_

from models import db, Property

class PropertyResource(Resource):
    def get(self, id=None):
        if id:
            property = Property.query.filter_by(id=id).first()
            
            if property:
                return property.to_dict(), 200
            else:
                return {"message": "property not found"}, 404
        
        else:
            properties = [n.to_dict() for n in Property.query.all() ]
            reponse = make_response(jsonify(properties), 200)
            return reponse
        
    def delete(self, id):
        property = Property.query.get_or_404(id)
        db.session.delete(property)
        db.session.commit()
        return {'message': "Property deleted"}, 200
    
    def post(self):
        data = request.get_json()
        
        new_property = Property(
            name = data["name"],
            image = data["image"],
            description = data["description"],
            price = data["price"],
            status = data["status"]
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        return {"message" : "Property created successfully"}, 201
            