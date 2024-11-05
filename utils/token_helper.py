from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def generate_token(payload: dict):
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM")
    return jwt.encode(payload, secret, algorithm=algorithm)

def validate_token(token: str):
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM")
    return jwt.decode(token, secret, algorithms=[algorithm])