from fastapi.encoders import jsonable_encoder
from config.db_connection import PostgresConnection
from schemas.event_schema import Event, EventDisplay, EventEdit


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
                tables=row[7],
                img_url=row[8]
            )
            result.append(event)
        return jsonable_encoder(result)

    def get(self, event_id: int):
        query = "SELECT * FROM events WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        row = self.cursor.fetchone()
        if not row:
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
        return jsonable_encoder(event)

    def create(self, new_event: Event):
        query = "INSERT INTO events (name, description, start_date, end_date, start_time, end_time, tables, img_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING event_id"
        self.cursor.execute(query, (
            new_event.name,
            new_event.description,
            new_event.start_date,
            new_event.end_date,
            new_event.start_time,
            new_event.end_time,
            new_event.tables,
            new_event.img_url
        ))
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
    
    def update(self, event: EventEdit):
        # Verify if the event exists
        query = "SELECT * FROM events WHERE event_id = %s"
        self.cursor.execute(query, (event.event_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Event not found"
            }
        # If the event exists delete all tables
        query = "DELETE FROM tables_event WHERE event_id = %s"
        self.cursor.execute(query, (event.event_id,))
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Tables couldn't be deleted"
            }
        # Update info
        query = "UPDATE events SET name = COALESCE(%s, name), description = COALESCE(%s, description), start_date = COALESCE(%s, start_date), end_date = COALESCE(%s, end_date), start_time = COALESCE(%s, start_time), end_time = COALESCE(%s, end_time), tables = COALESCE(%s, tables), img_url = COALESCE(%s, img_url) WHERE event_id = %s"
        self.cursor.execute(query, (
            event.name,
            event.description,
            event.start_date,
            event.end_date,
            event.start_time,
            event.end_time,
            event.tables,
            event.img_url,
            event.event_id,
        ))
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Event couldn't be updated"
            }
        # Create new tables
        table_list = []
        for table_num in range(1, event.tables + 1):
            table_list.append((table_num, event.event_id))
        query = "INSERT INTO tables_event (table_num, event_id) VALUES (%s, %s)"
        self.cursor.executemany(query, table_list)
        self.conn.commit()
        row_affected = self.cursor.rowcount
        self.cursor.close()
        if row_affected > 0:
            return {
                "error": False,
                "details": "Event updated successfully"
            }
        else:
            return {
                "error": True,
                "details": "Event couldn't be updated"
            }