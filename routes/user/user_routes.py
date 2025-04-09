from domain.services.user_service import UserService

class UserRoutes:
    def __init__(self, app, user_service: UserService):
        self.app = app
        self.user_service = user_service
    
    def post_user(self, json_data):
        return self.user_service.create_user(json_data)
    
    def get_user(self, user_id=None):
        user = self.user_service.get_user(user_id)
        print(user)
        return user