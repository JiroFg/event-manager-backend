import traceback
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from controllers.event_controller import EventController

router = APIRouter(prefix="/event", tags=["event"])

@router.get("/")
def get_all():
    try:
        event_controller = EventController()
        result = event_controller.get_all()
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
def create_event():
    try:
        event_controller = EventController()
        result = event_controller.create()
        return JSONResponse(
            content=result,
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )