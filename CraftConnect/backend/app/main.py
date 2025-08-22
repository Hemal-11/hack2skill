import os
from fastapi import FastAPI
from app.config.settings import settings
from app.routes import copilot

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS

app = FastAPI(
    title="CraftConnect AI API",
    description="The backend service for the CraftConnect marketplace."
)


app.include_router(copilot.router)      # Include your routers

@app.get("/")
def read_root():
    return {"message": "CraftConnect API is running"}