import os
import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
import uvicorn
import glob
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
#if settings.BACKEND_CORS_ORIGINS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:4200", "http://localhost:8070"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
async def job_function():
    my_files = [f for f in glob.glob("files/*.pdf")]

    for file in my_files:
        os.remove(file)


class SchedulerService:
    def __init__(self):
        self.sch = None

    def start(self):
        self.sch = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        self.sch.start()
        self.sch.add_job(job_function, 'cron', day_of_week='mon-fri', hour=20, minute=50, start_date='2022-12-02')


@app.on_event("startup")
async def run_scheduler():
    shed = SchedulerService()
    shed.start()

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True, reload_excludes="*.pdf")