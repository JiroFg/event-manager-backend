from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.db_connection import PostgresConnection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
)

@app.get("/")
def hello_world():
    return JSONResponse(content={"detials": "Hello World!"}, status_code=status.HTTP_200_OK)

@app.get("/test")
def test_db():
    try:
        conn = PostgresConnection.get_instance()
        return JSONResponse(content={"detials": "Everything is fine"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"details": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
