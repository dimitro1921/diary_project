from fastapi import FastAPI
from api.routes import router
from api.scheduler import start_scheduler

app = FastAPI(
    title="Personal Knowledge & Reflection Diary API",
    version="0.1.0"
)

# Include all API routes
app.include_router(router)

# Start the daily reflection prompt scheduler
start_scheduler()
