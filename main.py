from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, login_router, catalog_router, company_router, event_router, product_router, table_router, participation_router, schedule_router, meeting_router


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
app.include_router(company_router.router)
app.include_router(event_router.router)
app.include_router(product_router.router)
app.include_router(table_router.router)
app.include_router(participation_router.router)
app.include_router(schedule_router.router)
app.include_router(meeting_router.router)
