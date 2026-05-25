from ...db_connect import DbConnect

class InsertBase(DbConnect):
    def __init__(self):
        super().__init__()
        self.conn = self.connect()

    def insert_all_from_df(self, df, table_name):
        inserted_rows = df.to_sql(table_name, self.conn, if_exists="append", index=False)
        if inserted_rows:
            print(inserted_rows)
        else:
            print("No Rows Inserted")
        return inserted_rows