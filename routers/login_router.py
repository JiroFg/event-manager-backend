import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schemas.user_schema import UserLogin
from controllers.user_controller import UserController
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["login"])

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_controller = UserController()
        result = user_controller.login(form_data.username, form_data.password)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(
            content={"error": True, "details": str(e)},
            status_code=status.HTTP_200_OK
        )