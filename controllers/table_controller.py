from fastapi.encoders import jsonable_encoder
from schemas.table_schema import TableDisplay
from config.db_connection import PostgresConnection
from schemas.table_schema import ExtraTables, TableDisplay
from schemas.event_schema import EventDisplay


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

    def create_extra_tables(self, extra_tables: ExtraTables):
        # validate if event exists
        query = "SELECT * FROM events WHERE event_id = %s"
        self.cursor.execute(query, (extra_tables.event_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Event not found"
            }
        event = EventDisplay(
            event_id=row[0],
            name=row[1],
            description=row[2],
            start_date=row[3],
            end_date=row[4],
            start_time=row[5],
            end_time=row[6],
            tables=row[7],
            img_url=row[8]
        )
        # get the last table num
        query = "SELECT * FROM tables_event WHERE event_id = %s ORDER BY table_num DESC LIMIT 1"
        self.cursor.execute(query, (extra_tables.event_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Table not found"
            }
        last_table = TableDisplay(
            table_id=row[0],
            table_num=row[1],
            event_id=row[2],
            user_id=row[3]
        )
        # create extra tables
        last_table = last_table.table_num
        table_list = []
        for table_num in range(last_table + 1, last_table + extra_tables.tables + 1):
            table_list.append((table_num, extra_tables.event_id))
        query = "INSERT INTO tables_event (table_num, event_id) VALUES (%s, %s)"
        self.cursor.executemany(query, table_list)
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Tables couldn't be created"
            }
        # update tables in event
        current_tables = event.tables + extra_tables.tables
        query = "UPDATE events SET tables = %s WHERE event_id = %s"
        self.cursor.execute(query, (current_tables, event.event_id))
        row_affected = self.cursor.rowcount
        self.conn.commit()
        self.cursor.close()
        if not row_affected > 0:
            return {
                "error": True,
                "details": "Event couldn't be update"
            }
        else:
            return {
                "error": False,
                "details": "Tables added successfully"
            }
    
    def delete_table(self, table_id: int):
        # get table
        query = "SELECT * FROM tables_event WHERE table_id = %s"
        self.cursor.execute(query, (table_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Table not found"
            }
        table = TableDisplay(
            table_id=row[0],
            table_num=row[1],
            event_id=row[2],
            user_id=row[3]
        )
        # delete table
        query = "DELETE FROM tables_event WHERE table_id = %s"
        self.cursor.execute(query, (table_id,))
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Table couldn't be deleted"
            }
        # get event
        query = "SELECT * FROM events WHERE event_id = %s"
        self.cursor.execute(query, (table.event_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Event not found"
            }
        event = EventDisplay(
            event_id=row[0],
            name=row[1],
            description=row[2],
            start_date=row[3],
            end_date=row[4],
            start_time=row[5],
            end_time=row[6],
            tables=row[7],
            img_url=row[8]
        )
        # update event
        query = "UPDATE events SET tables = %s WHERE event_id = %s"
        self.cursor.execute(query, (event.tables - 1, event.event_id))
        row_affected = self.cursor.rowcount
        self.cursor.close()
        self.conn.commit()
        if row_affected > 0:
            return {
                "error": False,
                "details": "Table deleted successfully"
            }
        else:
            return {
                "error": True,
                "details": "Table couldn't be deleted"
            }
