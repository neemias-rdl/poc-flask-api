from data.repositories.user_repository import UserRepository


class Database:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_tables(self):
        self.user_repository.create_table()
        # Add other table creation methods here