from domain.entities.user import User


class UserRepository:

    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
    CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);
    """

    INSERT_USER = """
    INSERT INTO users (username, password, first_name, last_name, phone_number)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """

    SELECT_USER_BY_ID = """
    SELECT * FROM users WHERE id = %s;
    """

    SELECT_USER_BY_USERNAME = """
    SELECT * FROM users WHERE username = %s;
    """

    GET_ALL_USERS = """
    SELECT * FROM users;
    """

    DELETE_USER_BY_ID = """
    DELETE FROM users WHERE id = %s;
    """

    def __init__(self, connection):
        self.connection = connection


    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(UserRepository.CREATE_TABLE)
            self.connection.commit()
            return True

    def get_all_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(UserRepository.GET_ALL_USERS)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                user = User(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    phone_number=row[5]
                )

                users.append(user)
            return users

    def get_user_by_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(UserRepository.SELECT_USER_BY_ID, (user_id,))
            row = cursor.fetchone()
            if row:
                return 
            else:
                return None
            
    def get_user_by_username(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(UserRepository.SELECT_USER_BY_USERNAME, (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    phone_number=row[5]
                )
            else:
                return None

    def create_user(self, user: User):
        username = user.username
        password = user.password
        first_name = user.first_name
        last_name = user.last_name
        phone_number = user.phone_number

        with self.connection.cursor() as cursor:
            cursor.execute(UserRepository.INSERT_USER, (username, password, first_name, last_name, phone_number))
            user_id = cursor.fetchone()[0]
            self.connection.commit()
            return user_id
        
    def delete_user_by_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(UserRepository.DELETE_USER_BY_ID, (user_id,))
            self.connection.commit()
            return True
        return False