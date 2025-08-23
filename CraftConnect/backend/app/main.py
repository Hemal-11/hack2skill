import os
from fastapi import FastAPI
import vertexai
from contextlib import asynccontextmanager
from app.config.settings import settings
                     # ------  feature import ------ 
from app.routes import storyteller, translation, copilot, pricing, recommender

# ------------------------------------------------------------------

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS




app = FastAPI(
    title="CraftConnect AI API",
    description="The backend service for the CraftConnect marketplace."
)

vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)

app.include_router(copilot.router)      # Include your routers
app.include_router(storyteller.router, prefix="/storyteller", tags=["Storyteller"])    # storyteller router
app.include_router(translation.router, prefix="/translation")             # translation router
app.include_router(pricing.router, prefix="/pricing")               # pricing router
app.include_router(recommender.router, prefix="/recs", tags=["Recommendations"])     # recommender router


@app.get("/")
def read_root():
    return {"message": "CraftConnect API is running"}