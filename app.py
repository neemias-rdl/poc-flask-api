import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask
from helpers.connection_helper import parse_connection_url

load_dotenv()

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")
parsed_url_dict = parse_connection_url(url)
connection = psycopg2.connect(**parsed_url_dict)