import sqlite3
from pathlib import Path


class DbConnect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.base_dir = Path(__file__).resolve().parent.parent

        self.resources_dir = self.base_dir / "resources"
        self.resources_dir.mkdir(exist_ok=True)

        self.db_path = self.resources_dir / db_name

    def create_db_file_if_not_exists(self):
        if self.db_path.exists():
            print(f"Database already exists: {self.db_path}")
        else:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            print(f"Created database: {self.db_path}")

    def connect(self):
        return sqlite3.connect(self.db_path)