from domain.enums.roles import Role

class User:
    def __init__(self, id, username, password, first_name, last_name, phone_number, role: Role):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.role = role