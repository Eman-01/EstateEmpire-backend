from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models import db, UnitType

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')

class UnitTypeResource(Resource):
    def get(self, id=None):
        if id:
            unit_type = UnitType.query.filter_by(id=id).first()
            
            if unit_type:
                # Return a single unit type in the expected format
                return make_response(jsonify({"id": unit_type.id, "name": unit_type.name}), 200)
            else:
                return {"message": "Unit type not found"}, 404
        else:
            # Return a list of unit types
            unit_types = [{"id": n.id, "name": n.name} for n in UnitType.query.all()]
            response = make_response(jsonify({"propertyTypes": unit_types}), 200)
            return response

    def post(self):
        args = parser.parse_args()
        
        new_unit_type = UnitType(
            name=args['name']
        )
        db.session.add(new_unit_type)
        db.session.commit()
        
        # Return a response indicating success and the created unit type
        return make_response(jsonify({"message": "New unit type created successfully", "unit_type": {"id": new_unit_type.id, "name": new_unit_type.name}}), 201)
