from urllib.parse import urlparse

def parse_connection_url(base_url):
    parsed_url = urlparse(base_url)

    return {
        'dbname': parsed_url.path[1:],
        'user': parsed_url.username,
        'password': parsed_url.password,
        'port': parsed_url.port,
        'host': parsed_url.hostname
    }
