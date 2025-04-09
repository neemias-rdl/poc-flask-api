import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask
from helpers.connection_helper import parse_connection_url
from data.database.database import create_database

app = Flask(__name__)

def setup_environment():
    load_dotenv()
    url = os.environ.get("DATABASE_URL")
    parsed_url_dict = parse_connection_url(url)
    connection = psycopg2.connect(**parsed_url_dict)
    return connection

def create_app():
    connection = setup_environment()

    # Create database tables
    create_database(connection)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)