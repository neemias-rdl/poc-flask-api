import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse
from flask import Flask

def parse_connection_url(base_url):
    parsed_url = urlparse(base_url)

    return {
        'dbname': parsed_url.path[1:],
        'user': parsed_url.username,
        'password': parsed_url.password,
        'port': parsed_url.port,
        'host': parsed_url.hostname
    }


load_dotenv()

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")
print(url)

parsed_url_dict = parse_connection_url(url)

print(parsed_url_dict)

connection = psycopg2.connect(**parsed_url_dict)