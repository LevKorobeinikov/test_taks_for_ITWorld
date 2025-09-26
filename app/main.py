from fastapi import FastAPI

from app.api.routers import api_router
from app.core.config import settings
from app.core.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)


@app.on_event('startup')
async def on_startup():
    await init_db()


@app.get('/')
async def root():
    return ({'service': settings.PROJECT_NAME})
