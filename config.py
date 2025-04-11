from data.database.database import Database
from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from domain.services.jwt_service import JWTService
from helpers.app_di import AppDI
from routes.dtos.user_dto import UserDto
import os
from datetime import timedelta

def create_db(di: AppDI):
    repositories = di.get_all_repositories()
    database = Database(repositories=repositories)
    database.create_tables()

def configure_di(connection) -> AppDI:
    di = AppDI()

    # Repositories
    di.register_repository("user_repository", UserRepository(connection=connection))
    user_repository = di.get_repository("user_repository")
    
    # Services
    di.register_service("user_service", UserService(user_repository=user_repository))
    
    # JWT Service
    jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
    jwt_access_token_expires = timedelta(hours=1)
    jwt_refresh_token_expires = timedelta(days=30)
    di.register_service("jwt_service", JWTService(
        secret_key=jwt_secret_key,
        access_token_expires=jwt_access_token_expires,
        refresh_token_expires=jwt_refresh_token_expires
    ))

    # DTOs
    di.register_dto("user_dto", UserDto())

    return di
