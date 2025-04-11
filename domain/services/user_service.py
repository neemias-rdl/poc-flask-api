from data.repositories.user_repository import UserRepository
from domain.entities.user import User
from helpers.auth.auth import check_password, get_hashed_password

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None
        
        if check_password(password, user.password):
            return user
        
        return None

    def get_user(self, user_id=None):
        if user_id:
            return self.user_repository.get_user_by_id(user_id)
        return self.user_repository.get_all_users()
    
    def create_user(self, user_data):

        hashed_password = get_hashed_password(user_data['password'])

        user = User(
            id=None,
            username= user_data['username'],
            password= hashed_password.decode('utf8'),
            first_name= user_data['first_name'],
            last_name= user_data['last_name'],
            phone_number= user_data['phone_number']
        )

        return self.user_repository.create_user(user)
    
    def delete_user_by_id(self, user_id):
        return self.user_repository.delete_user_by_id(user_id)