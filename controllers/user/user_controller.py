from data.repositories.user_repository import UserRepository
from domain.enums.roles import Role
from domain.services.user_service import UserService    
from flask import Blueprint, jsonify, request

from helpers.auth.route_decorators import jwt_required, role_required
from controllers.dtos.user_dto import UserDto

def create_users_blueprint(di):
    users_bp = Blueprint("users", __name__)
    user_service: UserService = di.get_service("user_service")
    user_dto: UserDto = di.get_dto("user_dto")

    @users_bp.route("/", methods=["POST"])
    @jwt_required(di)
    def post_user():
        try:
            json_data = request.json 
            response = user_service.create_user(json_data)
            return jsonify({"message": "User created", "data": str(response)}), 200
        except Exception as e:
            return jsonify({"message": "Error creating user", "error": str(e)}), 500

    @users_bp.route("/", methods=["GET"])
    @jwt_required(di)
    @role_required(di, Role.ADMIN)
    def get_user():
        user_id = request.args.get("user_id")
        user = user_service.get_user(user_id)
        user_response = []
        for u in user:
            user_response.append(user_dto.to_json(u))
        return jsonify({"message": "Got User(s)", "data": str(user_response)}), 200

    @users_bp.route("/<int:user_id>", methods=["DELETE"])
    @jwt_required(di)
    @role_required(di, Role.ADMIN)
    def delete_user_by_id(user_id):
        user = user_service.delete_user_by_id(user_id)
        if user:
            return jsonify({"message": "User deleted", "data": str(user)}), 200
        else:
            return jsonify({"message": "User not found"}), 404
        
    return users_bp