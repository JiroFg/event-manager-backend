import traceback
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from controllers.user_controller import UserController
from middlewares.token_middleware import validate_token_middleware, validate_token_admin_middleware
from schemas.user_schema import User, UserEdit

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
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/admin/", dependencies=[Depends(validate_token_admin_middleware)])
def create_admin(new_user: User):
    try:
        user_controller = UserController()
        result = user_controller.create_admin(new_user)
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

@router.get("/", dependencies=[Depends(validate_token_admin_middleware)])
def get_all_users():
    try:
        user_controller = UserController()
        result = user_controller.get_all()
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

@router.get("/{user_id}", dependencies=[Depends(validate_token_middleware)])
def get_user(user_id: int):
    try:
        user_controller = UserController()
        result = user_controller.get(user_id)
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

#TODO
@router.post("/recovery/{token}")
def password_recovery():
    try:
        return JSONResponse(
            content={"details": "TODO"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/", dependencies=[Depends(validate_token_middleware)])
def update_user(user_edit: UserEdit):
    try:
        user_controller = UserController()
        result = user_controller.update(user_edit)
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