from typing import Annotated
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.db_connection import PostgresConnection
from routers import user_router, login_router, catalog_router
from middlewares.token_middleware import validate_token_middleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(user_router.router)
app.include_router(login_router.router)
app.include_router(catalog_router.router)

@app.get("/")
def hello_world():
    return JSONResponse(content={"detials": "Hello World!"}, status_code=status.HTTP_200_OK)

@app.get("/test", dependencies=[Depends(validate_token_middleware)])
def test_db():
    try:
        conn = PostgresConnection.get_instance()
        return JSONResponse(content={"detials": "Everything is fine"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"details": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
