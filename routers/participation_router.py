import traceback
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from controllers.participation_controller import ParticipationController
from schemas.participation_schema import ParticipationEdit, Participation, ParticipationDisplay
from middlewares.token_middleware import validate_token_middleware, validate_token_admin_middleware

router = APIRouter(prefix="/participation", tags=["participation"])

@router.post("/", dependencies=[Depends(validate_token_middleware)])
def register_participation(new_participation: Participation):
    try:
        participation_controller = ParticipationController()
        result = participation_controller.register_participation(new_participation)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error":True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{event_id}", dependencies=[Depends(validate_token_admin_middleware)], tags=["admin"])
def get_participations_by_event(event_id: int):
    try:
        participation_controller = ParticipationController()
        result = participation_controller.get_participations_by_event(event_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error":True, "details":str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/", dependencies=[Depends(validate_token_middleware)])
def update_participation(participation_edit: ParticipationEdit):
    try:
        participation_controller = ParticipationController()
        result = participation_controller.update_participation(participation_edit)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content=result,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )