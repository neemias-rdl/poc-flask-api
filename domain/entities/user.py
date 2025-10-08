from domain.enums.roles import Role


class User:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(
        self, id, username, password, first_name, last_name, phone_number, role: Role
    ):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "role": self.role.value if hasattr(self.role, "value") else self.role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            password=data.get("password"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone_number=data.get("phone_number"),
            role=(
                Role(data.get("role"))
                if data.get("role") in Role._value2member_map_
                else data.get("role")
            ),
        )
