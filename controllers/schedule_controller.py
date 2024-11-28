from fastapi.encoders import jsonable_encoder
from config.db_connection import PostgresConnection
from schemas.schedule_schema import ScheduleDisplay


class ScheduleController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()
    
    def get_schedule_by_event(self, event_id):
        result = []
        query = "SELECT * FROM schedules WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        rows = self.cursor.fetchall()
        for row in rows:
            schedule = ScheduleDisplay(
                schedule_id=row[0],
                event_id=row[1],
                start_time=row[2],
                end_time=row[3],
                day=row[4]
            )
            result.append(schedule)
        self.cursor.close()
        return jsonable_encoder(result)