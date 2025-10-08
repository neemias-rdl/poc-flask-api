import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from config import configure_di
from helpers.connection_helper import parse_connection_url
from controllers.user.auth_controller import create_auth_blueprint
from controllers.user.user_controller import create_users_blueprint


# TODO: Try to simplify this method or place it somewhere else
def setup_connection():
    load_dotenv()
    url = os.environ.get("DATABASE_URL")
    parsed_url_dict = parse_connection_url(url)
    # Add connection timeout settings
    parsed_url_dict["connect_timeout"] = 10  # 10 seconds connection timeout
    parsed_url_dict["options"] = "-c statement_timeout=5000"  # 5 seconds query timeout
    connection = psycopg2.connect(**parsed_url_dict)
    return connection


def create_app():
    # Create a Flask application instance
    app = Flask(__name__)
    connection = setup_connection()

    # Register services and repos in DI
    di = configure_di(connection)

    # Register blueprints
    # TODO: Move blueprint registration to a DI
    auth_bp = create_auth_blueprint(di)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    users_bp = create_users_blueprint(di)
    app.register_blueprint(users_bp, url_prefix="/users")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
