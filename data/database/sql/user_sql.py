INSERT_USER = """
INSERT INTO users (username, password, first_name, last_name, phone_number, role)
VALUES (%s, %s, %s, %s, %s, %s)
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
