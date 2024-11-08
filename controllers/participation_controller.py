from fastapi.encoders import jsonable_encoder
from schemas.participation_schema import Participation, ParticipationDisplay, ParticipationEdit
from config.db_connection import PostgresConnection


class ParticipationController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()

    def register_participation(self, new_participation: Participation):
        query = "INSERT INTO user_event_participation (user_id, event_id, accepted) VALUES (%s, %s, 'FALSE')"
        self.cursor.execute(query, (new_participation.user_id, new_participation.event_id))
        affected_row = self.cursor.rowcount
        self.cursor.close()
        if affected_row > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "Participation in event registered successfully"
            }
        else:
            return {
                "error": True,
                "details": "Participation in event couldn't be registered"
            }
    
    def get_participations_by_event(self, event_id: int):
        result = []
        query = "SELECT * FROM user_event_participation WHERE event_id = %s"
        self.cursor.execute(query, (event_id,))
        rows = self.cursor.fetchall()
        for row in rows:
            participation = ParticipationDisplay(
                participation_id=row[0],
                user_id=row[1],
                event_id=row[2],
                accepted=row[3]
            )
            result.append(participation)
        return jsonable_encoder(result)

    def update_participation(self, participation_edit: ParticipationEdit):
        # validate if participation exists
        query = "SELECT * FROM user_event_participation WHERE participation_id = %s"
        self.cursor.execute(query, (participation_edit.participation_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Participation couldn't be updated"
            }
        # update participation
        query = "UPDATE user_event_participation SET user_id = COALESCE(%s, user_id), event_id = COALESCE(%s, event_id), accepted = COALESCE(%s, accepted) WHERE participation_id = %s"
        self.cursor.execute(query, (participation_edit.user_id, participation_edit.event_id, participation_edit.accepted, participation_edit.participation_id))
        row_affected = self.cursor.rowcount
        self.cursor.close()
        if row_affected > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "Participation updated successfully"
            }
        else:
            return {
                "error": True,
                "details": "Participation couldn't be updated"
            }