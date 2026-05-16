import sqlite3

class DbConnect:
    def __init__(self):
        self.db_path = "C:/Users/riley/Desktop/InsiderTrading/edgar/resources/edgar.db"

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn