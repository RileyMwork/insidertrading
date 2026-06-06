from infrastructure.repository.sql.insert.insert_base import InsertBase

class EdgarInsert(InsertBase):
    def __init__(self):
        super().__init__()

    def insert_all_transactions(self, df):
        inserted_rows = self.insert_all_from_df(df, "insider_transactions")

        return inserted_rows