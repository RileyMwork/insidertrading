from ...db_connect import DbConnect

class SelectBase(DbConnect):
    def __init__(self):
        super().__init__()
        self.conn = self.connect()

    def select(self, select_columns, table_name, where_columns = [], where_values = [], order_by_column = None, order_by_direction = None, limit = None):
        cursor = self.conn.cursor()

        if where_columns and where_values:
            where_clause = "WHERE " + " AND ".join([f"{col} = ?" for col in where_columns])
        else:
            where_clause = ""

        if order_by_column:
            order_by_clause = f"ORDER BY {order_by_column}"
            if order_by_direction:
                order_by_clause += f" {order_by_direction}"
        else:
            order_by_clause = ""

        if limit:
            limit_clause = f"LIMIT {limit}"
        else:
            limit_clause = ""

        statement = f"SELECT {', '.join(select_columns)} FROM {table_name} {where_clause} {order_by_clause} {limit_clause}"

        cursor.execute(statement, where_values)
        row = cursor.fetchone()

        print(f"Selected Data: {row}")
        return row          