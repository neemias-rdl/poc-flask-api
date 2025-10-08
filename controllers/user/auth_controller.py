from http import HTTPStatus
from flask import Blueprint, jsonify, request

from domain.entities.user import User
from domain.enums.roles import Role
from domain.services.user_service import UserService
from domain.services.jwt_service import JWTService
from helpers.auth.route_decorators import jwt_required
from controllers.dtos.user_dto import UserDto

# TODO: Remove business logic from auth controller


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
        return jsonify(response.to_dict()), response.status

    @auth_bp.route("/login/", methods=["POST"])
    def login():
        json_data = request.json
        response = user_service.login(json_data["username"], json_data["password"])
        if response.status == HTTPStatus.OK:
            userDict = response.data
            user = User.from_dict(userDict)
            # Generate JWT tokens
            access_token = jwt_service.create_access_token(user)
            refresh_token = jwt_service.create_refresh_token(user)

            return (
                jsonify(
                    {
                        "message": "Login successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                        },
                    }
                ),
                HTTPStatus.OK,
            )

        return jsonify({"message": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED

    @auth_bp.route("/refresh/", methods=["POST"])
    def refresh():
        json_data = request.json
        refresh_token = json_data.get("refresh_token")

        if not refresh_token:
            return (
                jsonify({"message": "Refresh token is required"}),
                HTTPStatus.BAD_REQUEST,
            )

        # Validate the refresh token
        payload = jwt_service.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return (
                jsonify({"message": "Invalid refresh token"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Get the user from the token
        user_id = payload.get("user_id")
        user = user_service.get_user(user_id)

        if not user:
            return (
                jsonify({"message": "User not found"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Generate new access token
        access_token = jwt_service.create_access_token(user)

        return (
            jsonify(
                {
                    "message": "Token refreshed",
                    "access_token": access_token,
                }
            ),
            HTTPStatus.OK,
        )

    @auth_bp.route("/current_user/", methods=["GET"])
    @jwt_required(di)
    def current_user():
        user_id = request.user_id
        response = user_service.get_user(user_id)

        return jsonify(response.to_dict()), response.status

    return auth_bp
