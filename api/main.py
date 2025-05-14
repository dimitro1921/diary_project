from fastapi import FastAPI
from api.routes import router
from api.scheduler import start_scheduler
from app.db import Base, engine
from app.models import Entry

app = FastAPI(
    title="Personal Knowledge & Reflection Diary API",
    version="0.1.0"
)

# Include all API routes
app.include_router(router)

Base.metadata.create_all(bind=engine)

# Start the daily reflection prompt scheduler
start_scheduler()
