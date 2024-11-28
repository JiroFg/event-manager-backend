import traceback
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from controllers.schedule_controller import ScheduleController

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/{event_id}")
def get_schedule_by_event(event_id: int):
    try:
        schedule_controller = ScheduleController()
        result = schedule_controller.get_schedule_by_event(event_id)
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