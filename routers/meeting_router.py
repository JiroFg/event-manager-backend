import traceback
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from controllers.meeting_controller import MeetingController
from schemas.meeting_schema import Meeting

router = APIRouter(prefix="/meeting", tags=["meeting"])

@router.get("/{event_id}/{user_id}")
def get_meetings_by_event_user(event_id: int, user_id: int):
    try:
        meeting_controller = MeetingController()
        result = meeting_controller.get_meetings_by_event_user(event_id, user_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/")
def create_meeting(new_meeting: Meeting):
    try:
        meeting_controller = MeetingController()
        result = meeting_controller.create(new_meeting)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )