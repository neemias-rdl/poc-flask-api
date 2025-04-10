from data.repositories.user_repository import UserRepository
from helpers.app_di import AppDI


class Database:
    def __init__(self, repositories):
        self.repositories = repositories
    
    def create_tables(self):
        # Create tables using the repositories
        for repo in self.repositories.values():
            repo.create_table()