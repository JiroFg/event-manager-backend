from fastapi.encoders import jsonable_encoder
from schemas.meeting_schema import Meeting, MeetingDisplay
from config.db_connection import PostgresConnection
from schemas.schedule_schema import ScheduleDisplay
from schemas.user_schema import UserDisplay


class MeetingController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()

    def create(self, new_meeting: Meeting):
        # validate if buyer exists
        query = "SELECT * FROM users WHERE user_id = %s AND user_type_id = 1"
        self.cursor.execute(query, (new_meeting.buyer_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Buyer doesn't exist"
            }
        # validate if exhibitor exists
        query = "SELECT * FROM users WHERE user_id = %s AND user_type_id = 2"
        self.cursor.execute(query, (new_meeting.exhibitor_id,))
        row = self.cursor.fetchone()
        if not row: 
            self.cursor.close()
            return {
                "error": True,
                "details": "Exhibitor doesn't exist"
            }
        # validate if buyer already has a meeting in this schedule time
        query = "SELECT * FROM meetings WHERE buyer_id = %s AND schedule_id = %s"
        self.cursor.execute(query, (new_meeting.buyer_id, new_meeting.schedule_id))
        row = self.cursor.fetchone()
        if row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Buyer already has a meeting at that schedule"
            }
        # validate if schedule belongs to event
        query = "SELECT * FROM schedules WHERE schedule_id = %s"
        self.cursor.execute(query, (new_meeting.schedule_id,))
        row = self.cursor.fetchone()
        if not row:
            return {
                "error": True,
                "details": "Schedule doesn't exist"
            }
        schedule = ScheduleDisplay(
            schedule_id=row[0],
            event_id=row[1],
            start_time=row[2],
            end_time=row[3],
            day=row[4]
        )
        if not schedule.event_id == new_meeting.event_id:
            return {
                "error": "Schedule doesn't belong to provided event"
            }
        # validate if exhibitor already has a meeting in this schedule time
        query = "SELECT * FROM meetings WHERE exhibitor_id = %s AND schedule_id = %s"
        self.cursor.execute(query, (new_meeting.exhibitor_id, new_meeting.schedule_id))
        row = self.cursor.fetchone()
        if row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Exhibitor already has a meeting at that schedule"
            }
        # insert the new meeting
        query = "INSERT INTO meetings (buyer_id, exhibitor_id, schedule_id, event_id) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (new_meeting.buyer_id, new_meeting.exhibitor_id, new_meeting.schedule_id, new_meeting.event_id))
        affected_row = self.cursor.rowcount
        self.cursor.close()
        if affected_row > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "Meeting created successfully"
            }
        else:
            return {
                "error": True,
                "details": "Meeting couldn't be created"
            }
    
    def get_meetings_by_event_user(self, event_id: int, user_id: int):
        result = []
        # validate if event exist
        query = "SELECT * FROM events WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Event doesn't exist"
            }
        # validate if buyer exist
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "User doesn't exist"
            }
        user = UserDisplay(
            user_id=row[0],
            username=row[1],
            email=row[2],
            user_type_id=row[3],
            company_id=row[4],
            is_active=row[5]
        )
        # get meeting by user_type
        if user.user_type_id == 1:
            query = "SELECT * FROM meetings WHERE buyer_id = %s AND event_id = %s"
        elif user.user_type_id == 2:
            query = "SELECT * FROM meetings WHERE exhibitor_id = %s AND event_id = %s"
        else:
            self.cursor.close()
            return {
                "error": True,
                "details": "Invalid user type"
            }
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            meeting = MeetingDisplay(
                meeting_id=row[0],
                buyer_id=row[1],
                exhibitor_id=row[2],
                schedule_id=row[3],
                event_id=row[4]
            )
            result.append(meeting)
        self.cursor.close()
        return jsonable_encoder(result)

    def delete(self, meeting_id: int):
        # validate if meeting exist
        query = "SELECT * FROM meetings WHERE meeting_id = %s"
        self.cursor.execute(query, (meeting_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Meeting doesn't exist"
            }
        # delete meeting
        query = "DELETE FROM meetings WHERE meeting_id = %s"
        self.cursor.execute(query, (meeting_id))
        affected_row = self.cursor.rowcount
        if not affected_row > 0:
            self.cursor.close()
            return {
                "error": True,
                "details": "Meeting couldn't be deleted"
            }
        else:
            self.conn.commit()
            self.cursor.close()
            return {
                "error": False,
                "details": "Meeting deleted succesfully"
            }