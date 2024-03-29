import os
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
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    print(settings.BACKEND_CORS_ORIGINS)
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True, reload_excludes="*.pdf")