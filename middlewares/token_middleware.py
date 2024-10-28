from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.token_helper import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def validate_token_middleware(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = validate_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return