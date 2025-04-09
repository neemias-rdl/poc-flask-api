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

def get_user_by_id(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute(SELECT_USER_BY_ID, (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'password': row[2],
                'first_name': row[3],
                'last_name': row[4],
                'phone_number': row[5]
            }
        else:
            return None

def insert_user(connection, username, password, first_name, last_name, phone_number):
    with connection.cursor() as cursor:
        cursor.execute(INSERT_USER, (username, password, first_name, last_name, phone_number))
        user_id = cursor.fetchone()[0]
        connection.commit()
        return user_id
    