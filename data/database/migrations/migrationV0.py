def migrate_to_v0(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    phone_number VARCHAR(15),
                    role VARCHAR(20) NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
                CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);
                """
        )
        connection.commit()
        return True
