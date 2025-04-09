from data.repositories.user_repository import UserRepository


class Database:
    def __init__(self, connection, user_repository: UserRepository):
        self.user_repository = user_repository
        self.connection = connection
    
    def create_tables(self):
        self.user_repository.create_table(self.connection)
        # Add other table creation methods here