from datetime import datetime, timedelta
import jwt
from domain.entities.user import User

class JWTService:
    def __init__(self, secret_key, access_token_expires, refresh_token_expires):
        self.secret_key = secret_key
        self.access_token_expires = access_token_expires
        self.refresh_token_expires = refresh_token_expires
    
    def create_access_token(self, user: User):
        """
        Create a new access token for the user
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.now(datetime.UTC) + self.access_token_expires,
            'iat': datetime.now(datetime.UTC),
            'type': 'access'
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def create_refresh_token(self, user: User):
        """
        Create a new refresh token for the user
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.now(datetime.UTC) + self.refresh_token_expires,
            'iat': datetime.now(datetime.UTC),
            'type': 'refresh'
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def is_token_valid(self, token):
        payload = self.decode_token(token)
        return payload is not None
    
    def get_user_id_from_token(self, token):
        payload = self.decode_token(token)
        if payload and 'user_id' in payload:
            return payload['user_id']
        return None 