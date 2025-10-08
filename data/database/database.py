from data.database.migrations.migrationV0 import migrate_to_v0


class Database:
    def __init__(self, version: int, connection):
        self.version = version
        self.connection = connection

    def create_tables(self):
        migrate_to_v0(connection=self.connection)
