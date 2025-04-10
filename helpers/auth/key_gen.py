import random
import string


def generate_secret_key() -> str:
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key = ''.join(random.choice(random_str) for _ in range(32))
    return key