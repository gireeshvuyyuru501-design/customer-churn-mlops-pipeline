from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Works locally and inside Docker
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"

FEATURE_COLUMNS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0.0",
    description="FastAPI inference service for the trained churn model.",
)


class ChurnRequest(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Customer Churn Prediction API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "model": "churn-classifier-champion",
    }


@app.post("/predict")
def predict(customer: ChurnRequest) -> dict[str, Any]:
    payload = customer.model_dump()

    row = pd.DataFrame(
        [[payload[column] for column in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS,
    )

    prediction = int(model.predict(row)[0])

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(row)[0][1])

    return {
        "prediction": "Churn" if prediction == 1 else "No Churn",
        "churn_probability": (
            round(probability, 4) if probability is not None else None
        ),
        "model": "churn-classifier-champion",
    }