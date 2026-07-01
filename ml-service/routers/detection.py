from fastapi import APIRouter
from pydantic import BaseModel
from ..services.ml_inference import predict_url

router = APIRouter(prefix="/api", tags=["detection"])


class URLRequest(BaseModel):
    url: str


class PredictionResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    message: str


@router.post("/predict", response_model=PredictionResponse)
def predict_url_endpoint(request: URLRequest):
    result = predict_url(request.url)
    return {
        "url": request.url,
        "is_phishing": result["is_phishing"],
        "confidence": result["confidence"],
        "message": "Phishing detected!" if result["is_phishing"] else "Looks safe."
    }