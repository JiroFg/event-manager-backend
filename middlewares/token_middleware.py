from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.token_helper import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def validate_token_middleware(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = validate_token(token)
    print(payload)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return payload

def validate_token_admin_middleware(payload: Annotated[dict, Depends(validate_token_middleware)]):
    user_type = payload.get("user_type_id")
    if user_type != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return payload