from domain.entities.user import User


class UserDto:    
    def to_json(self, user: User) -> dict:
        return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
        }