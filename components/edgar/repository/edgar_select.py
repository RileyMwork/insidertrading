import datetime
from components.infrastructure.repository.sql.select.select_base import SelectBase

class EdgarSelect(SelectBase):
    def __init__(self):
        super().__init__()
        self.table_name = "insider_transactions"

    def get_latest_pull_date(self):
        
        select_columns = ["date_pulled_from_edgar"]
        order_by_column = "date_pulled_from_edgar"
        order_by_direction = "DESC"
        limit = 1
        statement = self.select(select_columns, self.table_name, order_by_column=order_by_column, order_by_direction=order_by_direction, limit=limit)
        print(f"Latest Pull Date: {statement[0] if statement else None}")
        return statement[0] if statement else None
    
    def get_latest_data(self):
        sql = f"SELECT * FROM {self.table_name} WHERE date_pulled_from_edgar = (SELECT MAX(date_pulled_from_edgar) FROM {self.table_name});"
        rows, columns = self.select_raw(sql)
        return rows, columns
    
    def get_data_by_date(self, date):
        date = datetime.strptime(date, "%Y%m%d").date().isoformat()
        return self.select("*", self.table_name, "date_pulled_from_edgar", where_params=(date), limit=1)
    
    def get_all_distinct_filed_dates(self):
        rows, columns = self.select_raw("SELECT DISTINCT filed_date FROM insider_transactions ORDER BY filed_date DESC")
        return [row[0] for row in rows]


