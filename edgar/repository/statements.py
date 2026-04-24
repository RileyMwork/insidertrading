from .db_connect import DbConnect

class Statements(DbConnect):
    def __init__(self):
        super().__init__()

    def get_latest_pull_date(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT date_pulled_from_edgar FROM insider_transactions ORDER BY date_pulled_from_edgar DESC LIMIT 1")
        row = cursor.fetchone()
        print(f"Latest Pull Date: {row[0] if row else None}")
        return row[0] if row else None

    def insert_all_from_df(self, df):
        conn = self.connect()
        inserted_rows = df.to_sql("insider_transactions", conn, if_exists="append", index=False)
        if inserted_rows:
            print(inserted_rows)
        else:
            print("No Rows Inserted")
        return inserted_rows
    
    