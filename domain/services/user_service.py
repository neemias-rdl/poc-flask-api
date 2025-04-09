from data.repositories.user_repository import UserRepository
from domain.entities.user import User
import json

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data):
        parsed_user = json.loads(user_data)

        user = User(
            id=None,
            username=parsed_user['username'],
            password=parsed_user['password'],
            first_name=parsed_user['first_name'],
            last_name=parsed_user['last_name'],
            phone_number=parsed_user['phone_number']
        )

        return self.user_repository.create_user(user)

    def update_user(self, user_id, user_data):
        pass

    def delete_user(self, user_id):
        pass
    
    def get_user(self, user_id=None):
        if user_id:
            return self.user_repository.get_user_by_id(user_id)
        return self.user_repository.get_all_users()