from data.repositories.user_repository import UserRepository
from domain.enums.roles import Role
from domain.services.user_service import UserService
from flask import Blueprint, jsonify, request

from helpers.auth.route_decorators import jwt_required, role_required
from controllers.dtos.user_dto import UserDto
from helpers.response_template import ResponseTemplate


def create_users_blueprint(di):
    users_bp = Blueprint("users", __name__)
    user_service: UserService = di.get_service("user_service")
    user_dto: UserDto = di.get_dto("user_dto")

    @users_bp.route("/", methods=["POST"])
    @jwt_required(di)
    @role_required(di, Role.ADMIN)
    def post_user():
        json_data = request.json
        response: ResponseTemplate = user_service.create_user(json_data)
        return jsonify(response.to_dict()), response.status

    @users_bp.route("/", defaults={"user_id": None}, methods=["GET"])
    @users_bp.route("/<int:user_id>", methods=["GET"])
    @jwt_required(di)
    @role_required(di, Role.ADMIN)
    def get_user(user_id):
        response: ResponseTemplate = user_service.get_user(user_id)
        return jsonify(response.to_dict()), response.status

    @users_bp.route("/<int:user_id>", methods=["DELETE"])
    @jwt_required(di)
    @role_required(di, Role.ADMIN)
    def delete_user_by_id(user_id):
        response: ResponseTemplate = user_service.delete_user_by_id(user_id)
        return jsonify(response.to_dict()), response.status

    return users_bp
