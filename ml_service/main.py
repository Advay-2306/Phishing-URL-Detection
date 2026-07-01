from fastapi import FastAPI
from dotenv import load_dotenv
import os

from .database.session import init_db
from .routers.detection import router as detection_router
from .routers.admin import router as admin_router

load_dotenv()

app = FastAPI(title="Phishing URL Detector")

init_db()

@app.get("/")
def home():
    return {"status": "ML Service is running", "env_example": os.getenv("APP_NAME", "Not set")}

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(detection_router)
app.include_router(admin_router)