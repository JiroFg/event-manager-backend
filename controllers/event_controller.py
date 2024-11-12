from datetime import datetime, timedelta
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
                img_url=row[8],
                meeting_duration=row[9]
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
            img_url=row[8],
            meeting_duration=row[9]
        )
        return jsonable_encoder(event)

    def create(self, new_event: Event):
        query = "INSERT INTO events (name, description, start_date, end_date, start_time, end_time, tables, img_url, meeting_duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING event_id"
        self.cursor.execute(query, (
            new_event.name,
            new_event.description,
            new_event.start_date,
            new_event.end_date,
            new_event.start_time,
            new_event.end_time,
            new_event.tables,
            new_event.img_url,
            new_event.meeting_duration
        ))
        last_id = self.cursor.fetchone()[0]
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
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
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Tables couldn't be created"
            }
        # create schedule
        schedule_list = []
        start_date = datetime(new_event.start_date.year, new_event.start_date.month, new_event.start_date.day)
        end_date = datetime(new_event.end_date.year, new_event.end_date.month, new_event.end_date.day)
        while start_date <= end_date:
            start_time_aux = datetime(start_date.year, start_date.month, start_date.day, new_event.start_time.hour, new_event.start_time.minute, new_event.start_time.second)
            end_time_aux = datetime(start_date.year, start_date.month, start_date.day, new_event.end_time.hour, new_event.start_time.minute, new_event.end_time.second)
            while start_time_aux < end_time_aux:
                end_meeting = start_time_aux + timedelta(minutes=new_event.meeting_duration)
                schedule_list.append((last_id, start_time_aux.time(), end_meeting.time(), start_time_aux.date()))
                start_time_aux = end_meeting
            start_date = start_date + timedelta(days=1)
        query = "INSERT INTO schedules (event_id, start_time, end_time, day) VALUES (%s, %s, %s, %s)"
        self.cursor.executemany(query, schedule_list)
        row_affected = self.cursor.rowcount
        self.cursor.close()
        if row_affected > 0:
            self.conn.commit()
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
        if event.tables:
            query = "DELETE FROM tables_event WHERE event_id = %s"
            self.cursor.execute(query, (event.event_id,))
            row_affected = self.cursor.rowcount
            if not row_affected > 0:
                self.cursor.close()
                return {
                    "error": True,
                    "details": "Tables couldn't be deleted"
                }
        # If the event exists delete all schedules
        if event.start_date and event.end_date and event.start_time and event.end_time and event.meeting_duration:
            query = "DELETE FROM schedules WHERE event_id = %s"
            self.cursor.execute(query, (event.event_id,))
            row_affected = self.cursor.rowcount
            if not row_affected > 0:
                self.cursor.close()
                return {
                    "error": True,
                    "details": "Schedules couldn't be deleted"
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
        if event.tables:
            table_list = []
            for table_num in range(1, event.tables + 1):
                table_list.append((table_num, event.event_id))
            query = "INSERT INTO tables_event (table_num, event_id) VALUES (%s, %s)"
            self.cursor.executemany(query, table_list)
            row_affected = self.cursor.rowcount
            if not row_affected > 0:
                self.cursor.close()
                return {
                    "error": True,
                    "details": "Tables couldn't be created"
                }
        # Create new schedule
        if event.start_date and event.end_date and event.start_time and event.end_time and event.meeting_duration:
            schedule_list = []
            start_date = datetime(event.start_date.year, event.start_date.month, event.start_date.day)
            end_date = datetime(event.end_date.year, event.end_date.month, event.end_date.day)
            while start_date <= end_date:
                start_time_aux = datetime(start_date.year, start_date.month, start_date.day, event.start_time.hour, event.start_time.minute, event.start_time.second)
                end_time_aux = datetime(start_date.year, start_date.month, start_date.day, event.end_time.hour, event.start_time.minute, event.end_time.second)
                while start_time_aux < end_time_aux:
                    end_meeting = start_time_aux + timedelta(minutes=event.meeting_duration)
                    schedule_list.append((event.event_id, start_time_aux.time(), end_meeting.time(), start_time_aux.date()))
                    start_time_aux = end_meeting
                start_date = start_date + timedelta(days=1)
            query = "INSERT INTO schedules (event_id, start_time, end_time, day) VALUES (%s, %s, %s, %s)"
            self.cursor.executemany(query, schedule_list)
            row_affected = self.cursor.rowcount
            self.cursor.close()
            if not row_affected > 0:
                return {
                    "error": True,
                    "details": "Event couldn't be updated"
                }
        self.conn.commit()
        return {
            "error": False,
            "details": "Event updated successfully"
        }

    def delete(self, event_id: int):
        # delete tables
        query = "DELETE FROM tables_event WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        row_affected = self.cursor.rowcount
        if not row_affected > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Tables couldn't be deleted"
            }
        # delete user event participation
        # TODO
        # delete schedule
        # TODO
        # delete event
        query = "DELETE FROM events WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        row_affected = self.cursor.rowcount
        self.cursor.close()
        if row_affected > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "Event deleted successfully"
            }
        else:
            return {
                "error": True,
                "details": "Event couldn't be delete"
            }