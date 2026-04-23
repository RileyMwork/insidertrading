import sqlite3

class DbConnect:
    def __init__(self):
        self.db_path = "C:/Users/riley/Desktop/InsiderTrading/edgar/resources/edgar.db"

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    # def select(self):
    #     connection = self.connect()
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM insider_transactions")
    #     print(cursor.fetchall())
    #     connection.close()

    # def debug_tables(self):
    #     conn = self.connect()
    #     cursor = conn.cursor()

    #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    #     print(cursor.fetchall())

    #     conn.close()