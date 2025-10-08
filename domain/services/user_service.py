from http import HTTPStatus
from data.repositories.user_repository import UserRepository
from domain.entities.user import User
from helpers.auth.auth import check_password, get_hashed_password
from helpers.response_template import ResponseTemplate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, username, password):
        try:
            user = self.user_repository.get_user_by_username(username)
        except Exception as e:
            return ResponseTemplate(
                data=None,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Database error",
            ).to_dict()

        if not user:
            return ResponseTemplate(
                data=None,
                status=HTTPStatus.UNAUTHORIZED,
                message="Invalid credentials",
            ).to_dict()

        if check_password(password, user.password):
            return ResponseTemplate(
                data=user.to_dict(),
                status=HTTPStatus.OK,
                message="Login successful",
            ).to_dict()

        return ResponseTemplate(
            data=None,
            status=HTTPStatus.UNAUTHORIZED,
            message="Invalid credentials",
        ).to_dict()

    def get_user(self, user_id=None):
        try:
            if user_id:
                user = self.user_repository.get_user_by_id(user_id)
                if user:
                    return ResponseTemplate(
                        data=user.to_dict(),
                        status=HTTPStatus.OK,
                        message="User fetched successfully",
                    ).to_dict()

                return ResponseTemplate(
                    data=None,
                    status=HTTPStatus.NOT_FOUND,
                    message="User not found",
                ).to_dict()

        except Exception as e:
            return ResponseTemplate(
                data=None,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Database error",
            ).to_dict()

    def create_user(self, user_data):

        hashed_password = get_hashed_password(user_data["password"])

        user = User(
            id=None,
            username=user_data["username"],
            password=hashed_password.decode("utf8"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone_number=user_data["phone_number"],
            role=user_data["role"],
        )

        try:
            self.user_repository.create_user(user)
            return ResponseTemplate(
                data=user.to_dict(),
                status=HTTPStatus.CREATED,
                message="User created successfully",
            ).to_dict()
        except Exception as e:
            return ResponseTemplate(
                data=None,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Database error",
            ).to_dict()

    def delete_user_by_id(self, user_id):
        try:
            self.user_repository.delete_user_by_id(user_id)
            return ResponseTemplate(
                data={"user_id": user_id},
                status=HTTPStatus.OK,
                message="User deleted successfully",
            ).to_dict()
        except Exception as e:
            return ResponseTemplate(
                data=None,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Database error",
            ).to_dict()
