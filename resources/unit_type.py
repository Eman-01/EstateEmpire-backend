from flask_restful import Resource
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from sqlalchemy import and_, not_

from models import db, UnitType
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
class UnitTypeResource(Resource):
    def get(self, id=None):
        if id:
            unit_type = UnitType.query.filter_by(id=id).first()
            
            if unit_type:
                return unit_type.to_dict(), 200
            else:
                return {"message": "Unit type not found"}, 404
        else:
            unit_type = [n.to_dict() for n in UnitType.query.all() ]
            reponse = make_response(jsonify(unit_type), 200)
            return reponse
    def post(self):
        args = parser.parse_args()
        
        new_unit_type = UnitType(
            name = args['name']
        )
        db.session.add(new_unit_type)
        db.session.commit()
        
        return {"message": "New unit type created successfully", "unit_type": new_unit_type.to_dict()}, 201