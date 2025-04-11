import bcrypt
from flask import jsonify, request
from functools import wraps

from data.repositories.user_repository import UserRepository
from domain.services.jwt_service import JWTService
from helpers.app_di import AppDI

def authenticate(di: AppDI):
    user_repository: UserRepository = di.get_repository("user_repository")
    jwt_service: JWTService = di.get_service("jwt_service")
    
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Authentication required"}), 401
    
    user = user_repository.get_user_by_username(auth.username)
    if not user:
        return jsonify({"message": "User not found"}), 401
    
    if not check_password(auth.password, user.password):
        return jsonify({"message": "Invalid password"}), 401
    
    return user

def get_hashed_password(plain_text_password: str):
    encoded_password = plain_text_password.encode('utf-8')
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    encoded_password = plain_text_password.encode('utf-8')
    encoded_password_hash = hashed_password.encode('utf-8')
    return bcrypt.checkpw(encoded_password, encoded_password_hash)

# Protects routes that require authentication
def jwt_required(di: AppDI):
    def decorator(decorator_func):
        @wraps(decorator_func)
        def decorated_function(*args, **kwargs):
            jwt_service: JWTService = di.get_service("jwt_service")
            
            # Get the token from the Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"message": "Missing or invalid Authorization header"}), 401
            
            token = auth_header.split(' ')[1]
            
            # Validate the token
            if not jwt_service.is_token_valid(token):
                return jsonify({"message": "Invalid or expired token"}), 401
            
            # Get the user ID from the token
            user_id = jwt_service.get_user_id_from_token(token)
            if not user_id:
                return jsonify({"message": "Invalid token"}), 401
            
            # Add the user_id to the request context
            request.user_id = user_id
            
            return decorator_func(*args, **kwargs)
        return decorated_function
    return decorator