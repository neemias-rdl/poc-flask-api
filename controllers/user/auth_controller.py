from flask import Blueprint, jsonify, request

from domain.enums.roles import Role
from domain.services.user_service import UserService
from domain.services.jwt_service import JWTService
from helpers.auth.route_decorators import jwt_required
from controllers.dtos.user_dto import UserDto


def create_auth_blueprint(di):
    auth_bp = Blueprint("auth", __name__)
    user_service: UserService = di.get_service("user_service")
    jwt_service: JWTService = di.get_service("jwt_service")
    user_dto: UserDto = di.get_dto("user_dto")

    @auth_bp.route("/register/", methods=["POST"])
    def register():
        json_data = request.json
        json_data["role"] = Role.USER
        response = user_service.create_user(json_data)
        return jsonify({"message": "User created", "data": str(response)}), 200

    @auth_bp.route("/login/", methods=["POST"])
    def login():
        json_data = request.json 
        user = user_service.login(json_data["username"], json_data["password"])
        if user:
            # Generate JWT tokens
            access_token = jwt_service.create_access_token(user)
            refresh_token = jwt_service.create_refresh_token(user)
            
            return jsonify({
                "message": "Login successful", 
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }), 200
        
        return jsonify({"message": "Invalid credentials"}), 401
    
    @auth_bp.route("/refresh/", methods=["POST"])
    def refresh():
        json_data = request.json
        refresh_token = json_data.get("refresh_token")
        
        if not refresh_token:
            return jsonify({"message": "Refresh token is required"}), 400
        
        # Validate the refresh token
        payload = jwt_service.decode_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return jsonify({"message": "Invalid refresh token"}), 401
        
        # Get the user from the token
        user_id = payload.get('user_id')
        user = user_service.get_user(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 401
        
        # Generate new access token
        access_token = jwt_service.create_access_token(user)
        
        return jsonify({
            "message": "Token refreshed",
            "access_token": access_token
        }), 200
    
    @auth_bp.route("/current_user/", methods=["GET"])
    @jwt_required(di)
    def current_user():
        user_id = request.user_id
        user = user_service.get_user(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number
            }
        }), 200
        
    return auth_bp