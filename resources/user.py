from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

bcrypt = Bcrypt()

class SignupResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='Email address is required')
    parser.add_argument('password', required=True, help='Password is required')
    
    def post(self):
        data = self.parser.parse_args()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data['password'] = hashed_password
        
        email = User.query.filter_by(email=data['email']).first()
        if email:
            return {"message": "Email address already taken", "status": "fail"}, 422
        
        agent = User(email=data['email'], password_hash=data['password'])
        db.session.add(agent)
        db.session.commit()

        return {"message": "User registered successfully", "status": "success", "user": agent.to_dict()}

class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")
    
    def post(self):
        data = self.parser.parse_args()
        agent = User.query.filter_by(email=data['email']).first()

        if agent and bcrypt.check_password_hash(agent.password_hash, data['password']):
            agent_dict = agent.to_dict()

            access_token = create_access_token(identity=agent_dict['id'])
            
            return {"message": "Login successful", "status": "success", "user": agent_dict, "access_token": access_token}
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 403

    @jwt_required()
    def get(self):
        current_agent_id = get_jwt_identity()
        agent = User.query.get(current_agent_id)

        if agent:
            return {"message": "User profile fetched successfully", "status": "success", "user": agent.to_dict()}
        else:
            return {"message": "User not found", "status": "fail"}, 404