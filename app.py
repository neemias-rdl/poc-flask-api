import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from config import configure_di, create_db
from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from helpers.app_di import AppDI
from helpers.connection_helper import parse_connection_url
from data.database.database import Database
from controllers.dtos.user_dto import UserDto
from controllers.user.auth_controller import create_auth_blueprint
from controllers.user.user_controller import create_users_blueprint

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
    di = configure_di(connection)
    
    # Create the database and tables
    create_db(di)

    auth_bp = create_auth_blueprint(di)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    users_bp = create_users_blueprint(di)
    app.register_blueprint(users_bp, url_prefix="/users")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)