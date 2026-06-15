from components.infrastructure.repository.sql.insert.insert_base import InsertBase

class AlpacaInsert(InsertBase):
    def __init__(self):
        super().__init__()
        self.initial_order_info_columns = ["symbol",  "created_at", "expires_at", "order_type", "side", "time_in_force", 
                                            "ordered_qty", "filled_qty", "filled_avg_price", "take_profit", "stop_loss", "stop_price"]

    def insert_new_order_info(self, values):
        inserted_rows = self.insert("initial_order_info", self.initial_order_info_columns, values)

        return inserted_rows