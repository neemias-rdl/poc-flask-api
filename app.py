import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from helpers.app_di import AppDI
from helpers.connection_helper import parse_connection_url
from data.database.database import Database
from routes.dtos.user_dto import UserDto
from routes.user.user_routes import create_users_blueprint

BASE_URL = "marmitas-go-v0"

def setup_connection():
    load_dotenv()
    url = os.environ.get("DATABASE_URL")
    parsed_url_dict = parse_connection_url(url)
    connection = psycopg2.connect(**parsed_url_dict)
    return connection

def create_app():   
    # Create a Flask application instance
    app = Flask(__name__)
    connection = setup_connection()
    
    # Register services and repos in DI
    di = AppDI()
    di.register_repository("user_repository", UserRepository(connection=connection))
    user_repository = di.get_repository("user_repository")
    di.register_service("user_service", UserService(user_repository=user_repository))

    # Create the database and tables
    database = Database(user_repository=user_repository)
    database.create_tables()

    # Register DTOs in DI
    di.register_dto("user_dto", UserDto())

    # Create the tables
    users_bp = create_users_blueprint(di)
    app.register_blueprint(users_bp, url_prefix="/users")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)