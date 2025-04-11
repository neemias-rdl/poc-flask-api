# Protects routes that require authentication
from functools import wraps

from domain.enums.roles import Role
from helpers.app_di import AppDI
from domain.services.jwt_service import JWTService
from flask import request, jsonify  


def validate_token_from_header(req, jwt_service: JWTService):

    auth_header = req.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise jsonify({"message": "Missing or invalid Authorization header"}), 401
    
    token = auth_header.split(' ')[1]

    # Validate the token
    if not jwt_service.is_token_valid(token):
        raise jsonify({"message": "Invalid or expired token"}), 401

    return token
# Protects routes that require authentication
def jwt_required(di: AppDI):
    def decorator(decorator_func):
        @wraps(decorator_func)
        def decorated_function(*args, **kwargs):
            jwt_service: JWTService = di.get_service("jwt_service")

            try:
                token = validate_token_from_header(request, jwt_service)
            
                # Get the user ID from the token# Get the user ID from the token
                user_id = jwt_service.get_user_id_from_token(token)
                if not user_id:
                    return jsonify({"message": "Invalid token"}), 401
                
                # Add the user_id to the request context
                request.user_id = user_id
                
                return decorator_func(*args, **kwargs)
            
            except Exception as e:
                return e
        return decorated_function
    return decorator

# Protects routes that require a specific role
def role_required(di: AppDI, required_role: Role):
    def decorator(decorator_func):
        @wraps(decorator_func)
        def decorated_function(*args, **kwargs):
            jwt_service: JWTService = di.get_service("jwt_service")
            
            try:
                token = validate_token_from_header(request, jwt_service)

                # Get the user ID and role from the token
                payload = jwt_service.decode_token(token)
                if not payload or 'user_id' not in payload or 'role' not in payload:
                    return jsonify({"message": "Invalid token"}), 401
                
                user_id = payload['user_id']
                user_role = payload['role']
                
                # Check if the user has the required role
                if user_role != required_role.value:
                    return jsonify({"message": "Insufficient permissions"}), 403
                
                # Add the user_id to the request context
                request.user_id = user_id
                
                return decorator_func(*args, **kwargs)
            except Exception as e:
                return e
        return decorated_function
    return decorator