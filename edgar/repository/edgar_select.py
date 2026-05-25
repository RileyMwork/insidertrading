from infrastructure.repository.sql.select.select_base import SelectBase

class EdgarSelect(SelectBase):
    def __init__(self):
        super().__init__()
        self.table_name = "edgar_insider_transactions"

    def get_latest_pull_date(self):
        
        select_columns = ["date_pulled_from_edgar"]
        order_by_column = "date_pulled_from_edgar"
        order_by_direction = "DESC"
        limit = 1
        statement = self.select(select_columns, self.table_name, order_by_column=order_by_column, order_by_direction=order_by_direction, limit=limit)
        print(f"Latest Pull Date: {statement[0] if statement else None}")
        return statement[0] if statement else None
