from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from controllers.user_controller import UserController
from schemas.user_schema import User

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/")
def create_user(new_user: User):
    try:
        user_controller = UserController()
        result = user_controller.create(new_user)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )