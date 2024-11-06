import traceback
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from controllers.event_controller import EventController
from schemas.event_schema import Event, EventEdit
from middlewares.token_middleware import validate_token_admin_middleware

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

@router.get("/{event_id}")
def get_event(event_id: int):
    try:
        event_controller = EventController()
        result = event_controller.get(event_id)
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

@router.post("/", dependencies=[Depends(validate_token_admin_middleware)], tags=["admin"])
def create_event(new_event: Event):
    try:
        event_controller = EventController()
        result = event_controller.create(new_event)
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

@router.put("/", dependencies=[Depends(validate_token_admin_middleware)], tags=["admin"])
def edit_event(event: EventEdit):
    try:
        event_controller = EventController()
        result = event_controller.update(event)
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