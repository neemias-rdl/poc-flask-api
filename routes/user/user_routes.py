from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService    
from flask import Blueprint, jsonify, request

def create_users_blueprint(di):
    users_bp = Blueprint("users", __name__)
    user_service = di.get_service("user_service")

    @users_bp.route("/", methods=["POST"])
    def post_user():
        json_data = request.json 
        user = user_service.create_user(json_data)
        return jsonify({"message": "User created", "data": str(user)}), 200

    @users_bp.route("/", methods=["GET"])
    def get_user():
        user_id = request.args.get("user_id")
        user = user_service.get_user(user_id)
        return jsonify({"message": "Got User(s)", "data": str(user)}), 200

    return users_bp