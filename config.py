from data.database.database import Database
from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from helpers.app_di import AppDI
from helpers.auth.key_gen import generate_secret_key
from routes.dtos.user_dto import UserDto

SECRET_KEY = generate_secret_key()

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

    # DTOs
    di.register_dto("user_dto", UserDto())

    return di
