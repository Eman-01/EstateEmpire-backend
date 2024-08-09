from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from sqlalchemy import and_, not_
from models import db, Property, PropertyType, PropertyStatus

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('image', type=str, required=True, help='Image is required')
parser.add_argument('description', type=str, required=True, help='Description is required')
parser.add_argument('location', type=str, required=True, help='Location is required')
parser.add_argument('price', type=int, required=True, help='Price is required')
parser.add_argument('type', type=str, required=True, choices=('for_sale', 'for_rent'), help='Type must be either "for_sale" or "for_rent"')
parser.add_argument('units', type=int, required=True, help='Number of units is required')
parser.add_argument('unit_type_id', type=int, required=True, help='Unit type ID is required')

class PropertyResource(Resource):
    def get(self, id=None):
        if id:
            property = Property.query.filter_by(id=id).first()
            
            if property:
                return property.to_dict(), 200
            else:
                return {"message": "property not found"}, 404
        
        else:
            property = [n.to_dict() for n in Property.query.all() ]
            reponse = make_response(jsonify(property), 200)
            return reponse
        
    # def patch(self, id=None):
    #     args = parser.parse_args() 
    #     property = Property.query.filter_by(id = id).first()
        
    #     if property == None:
    #         return {'message': "Property not found"}, 404
        
    #     property.name = args['name']
    #     property.image = args['image']
    #     property.description = args['description']
    #     property.location = args['location']
    #     property.price = args['price']
    #     property.type = args['type'].lower()
    #     property.units = args['units']
    #     property.status = args['status'].lower()
        
    def post(self):
            args = parser.parse_args()
            new_property = Property(
                name=args['name'],
                image=args['image'],
                description=args['description'],
                location=args['location'],
                price=args['price'],
                type=args['type'].lower(),
                units=args['units'],
                unit_type_id=args['unit_type_id'],
                status='available' 
            )
            db.session.add(new_property)
            db.session.commit()
            return new_property.to_dict(), 201
        
    def delete(self, id):
        property = Property.query.get_or_404(id)
        db.session.delete(property)
        db.session.commit()
        return {'message': "Property deleted"}, 200
        
class PropertyForSaleResource(Resource):
    def get(self, id=None):
        if id:
            property = Property.query.filter_by(id=id, type=PropertyType.FOR_SALE).first()
            
            if property:
                return property.to_dict(), 200
            else:
                return {"message": "Property not found"}, 404
        
        else:
            properties = Property.query.filter_by(type=PropertyType.FOR_SALE).all()
            return jsonify([property.to_dict() for property in properties])

        
class PropertyForRentResource(Resource):
    def get(self, id=None):
        if id:
            property = Property.query.filter_by(id=id, type=PropertyType.FOR_RENT).first()
            
            if property:
                return property.to_dict(), 200
            else:
                return {"message": "property not found"}, 404
        
        else:
            properties = Property.query.filter_by(type=PropertyType.FOR_RENT).all()
            return jsonify([property.to_dict() for property in properties])