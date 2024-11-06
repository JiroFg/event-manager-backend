from fastapi.encoders import jsonable_encoder
from schemas.table_schema import TableDisplay
from config.db_connection import PostgresConnection


class TableController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()

    def get_tables_by_event(self, event_id: int):
        result = []
        query = "SELECT * FROM tables_event WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        rows = self.cursor.fetchall()
        for row in rows:
            table = TableDisplay(
                table_id=row[0],
                table_num=row[1],
                event_id=row[2],
                user_id=row[3]
            )
            result.append(table)
        self.cursor.close()
        return jsonable_encoder(result)
