# Creates all database tables
# and populates them with initial data
from data.daos.user_dao import CREATE_TABLE as CREATE_USER_TABLE

def create_tables(connection, statements):
    with connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)
            connection.commit()

def create_database(connection):
    # Create all tables
    create_tables(connection, [CREATE_USER_TABLE])