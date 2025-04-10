from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService    
from flask import Blueprint, jsonify, request

from routes.dtos.user_dto import UserDto

def create_users_blueprint(di):
    users_bp = Blueprint("users", __name__)
    user_service: UserService = di.get_service("user_service")
    user_dto: UserDto = di.get_dto("user_dto")

    @users_bp.route("/", methods=["POST"])
    def post_user():
        json_data = request.json 
        response = user_service.create_user(json_data)
        return jsonify({"message": "User created", "data": str(response)}), 200

    @users_bp.route("/", methods=["GET"])
    def get_user():
        user_id = request.args.get("user_id")
        user = user_service.get_user(user_id)
        user_response = []
        for u in user:
            user_response.append(user_dto.to_json(u))
        return jsonify({"message": "Got User(s)", "data": str(user_response)}), 200

    @users_bp.route("/<int:user_id>", methods=["DELETE"])
    def delete_user_by_id(user_id):
        user = user_service.delete_user_by_id(user_id)
        if user:
            return jsonify({"message": "User deleted", "data": str(user)}), 200
        else:
            return jsonify({"message": "User not found"}), 404
        
    return users_bp