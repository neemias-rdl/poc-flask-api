from data.database.sql.user_sql import (
    DELETE_USER_BY_ID,
    GET_ALL_USERS,
    INSERT_USER,
    SELECT_USER_BY_ID,
    SELECT_USER_BY_USERNAME,
)
from domain.entities.user import User


class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_all_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(GET_ALL_USERS)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                user = User.from_table_row(row)
                users.append(user)
            return users

    def get_user_by_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_USER_BY_ID, (user_id,))
            row = cursor.fetchone()
            if row:
                return User.from_table_row(row)
            else:
                return None

    def get_user_by_username(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_USER_BY_USERNAME, (username,))
            row = cursor.fetchone()
            if row:
                return User.from_table_row(row)
            else:
                return None

    def create_user(self, user: User):
        username = user.username
        password = user.password
        first_name = user.first_name
        last_name = user.last_name
        phone_number = user.phone_number
        role = user.role.value if hasattr(user.role, "value") else user.role

        with self.connection.cursor() as cursor:
            cursor.execute(
                INSERT_USER,
                (username, password, first_name, last_name, phone_number, role),
            )
            user_id = cursor.fetchone()[0]
            self.connection.commit()
            return user_id

    def delete_user_by_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(DELETE_USER_BY_ID, (user_id,))
            self.connection.commit()
            return True
        return False
