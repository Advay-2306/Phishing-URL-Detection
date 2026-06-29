from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Phishing URL Detector")

@app.get("/")
def home():
    return {"status": "ML Service is running", "env_example": os.getenv("APP_NAME", "Not set")}

@app.get("/health")
def health():
    return {"status": "healthy"}