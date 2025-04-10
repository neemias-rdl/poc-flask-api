import bcrypt
from flask import jsonify, request

from data.repositories.user_repository import UserRepository
from helpers.app_di import AppDI

def authenticate(di: AppDI):
    user_repository: UserRepository = di.get_repository("user_repository")
    
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Authentication required"}), 401
    
    user = user_repository.get_user_by_username(auth.username)
    if not user:
        return jsonify({"message": "User not found"}), 401
    
def get_hashed_password(plain_text_password: str):
    encoded_password = plain_text_password.encode('utf-8')
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    encoded_password = plain_text_password.encode('utf-8')
    encoded_password_hash = hashed_password.encode('utf-8')
    return bcrypt.checkpw(encoded_password, encoded_password_hash)