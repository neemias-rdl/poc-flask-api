from flask import Blueprint, jsonify, request

from domain.services.user_service import UserService
from routes.dtos.user_dto import UserDto


def create_auth_blueprint(di):
    auth_bp = Blueprint("auth", __name__)
    user_service: UserService = di.get_service("user_service")
    user_dto: UserDto = di.get_dto("user_dto")

    @auth_bp.route("/cadastro/", methods=["POST"])
    def cadastro():
        json_data = request.json 
        response = user_service.create_user(json_data)
        return jsonify({"message": "User created", "data": str(response)}), 200

    @auth_bp.route("/login/", methods=["POST"])
    def login():
        json_data = request.json 
        response = user_service.login(json_data["username"], json_data["password"])
        if response:
            return jsonify({"message": "Login successful", "data": str(response)}), 200
        
        return jsonify({"message": "Invalid credentials"}), 401
        
    return auth_bp