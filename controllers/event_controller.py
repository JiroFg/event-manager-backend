from fastapi.encoders import jsonable_encoder
from config.db_connection import PostgresConnection
from schemas.event_schema import Event, EventDisplay


class EventController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()

    def get_all(self):
        result = []
        query = "SELECT * FROM events"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            event = EventDisplay(
                event_id=row[0],
                name=row[1],
                description=row[2],
                start_date=row[3],
                end_date=row[4],
                start_time=row[5],
                end_time=row[6],
                tables=row[7]
            )
            result.append(event)
        return jsonable_encoder(result)

    def get(self, event_id: int):
        query = "SELECT * FROM events WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        row = self.cursor.fetchone()
        event = EventDisplay(
            event_id=row[0],
            name=row[1],
            description=row[2],
            start_date=row[3],
            end_date=row[4],
            start_time=row[5],
            end_time=row[6],
            tables=row[7]
        )
        return jsonable_encoder(event)

    def create(self, new_event: Event):
        query = "INSERT INTO events (name, description, start_date, end_date, start_time, end_time, tables) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING event_id"
        self.cursor.execute(query, (
            new_event.name,
            new_event.description,
            new_event.start_date,
            new_event.end_date,
            new_event.start_time,
            new_event.end_time,
            new_event.tables
        ))
        self.conn.commit()
        last_id = self.cursor.fetchone()[0]
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            return {
                "error": True,
                "details": "Event couldn't be created"
            }
        # create tables
        table_list = []
        for table_num in range(1, new_event.tables + 1):
            table_list.append((table_num, last_id))
        query = "INSERT INTO tables_event (table_num, event_id) VALUES (%s, %s)"
        self.cursor.executemany(query, table_list)
        self.conn.commit()
        row_affected = self.cursor.rowcount
        self.cursor.close()
        if row_affected > 0:
            return {
                "error": False,
                "details": "Event created successfully"
            }
        else:
            return {
                "error": True,
                "details": "Event couldn't be created"
            }