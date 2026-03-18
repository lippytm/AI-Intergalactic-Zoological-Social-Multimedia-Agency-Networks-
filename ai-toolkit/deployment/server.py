"""
Model Deployment Server
========================
FastAPI application that serves any scikit-learn or PyTorch model via REST.
"""

from __future__ import annotations

import logging
import os
import pickle
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(
    title="AI Model Server",
    description="Serves ML models via REST API",
    version="1.0.0",
)

# Global model store
_MODELS: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    features: list[list[float]]
    model_name: str = "default"


class PredictResponse(BaseModel):
    predictions: list[Any]
    probabilities: list[list[float]] | None = None


class LoadModelRequest(BaseModel):
    model_path: str
    model_name: str = "default"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "models_loaded": str(list(_MODELS.keys()))}


@app.post("/models/load")
def load_model(req: LoadModelRequest) -> dict[str, str]:
    """Load a pickled scikit-learn model from disk.

    WARNING: Only load models from trusted sources.  Pickle files can execute
    arbitrary code on deserialization.  In production, prefer joblib or ONNX.
    """
    path = Path(req.model_path).resolve()
    # Restrict to files within the current working directory
    cwd = Path.cwd().resolve()
    if not str(path).startswith(str(cwd)):
        raise HTTPException(status_code=400, detail="Model path must be inside the working directory.")
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    if path.suffix not in {".pkl", ".pickle", ".joblib"}:
        raise HTTPException(status_code=400, detail="Only .pkl, .pickle, or .joblib files are accepted.")
    with open(path, "rb") as f:
        _MODELS[req.model_name] = pickle.load(f)  # noqa: S301
    logger.info("Loaded model %r from %s", req.model_name, path)
    return {"message": f"Model {req.model_name!r} loaded successfully."}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    """Run inference with the named model."""
    if req.model_name not in _MODELS:
        raise HTTPException(status_code=404, detail=f"Model {req.model_name!r} not loaded.")
    model = _MODELS[req.model_name]
    X = np.array(req.features)
    preds = model.predict(X).tolist()
    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X).tolist()
    return PredictResponse(predictions=preds, probabilities=proba)


@app.get("/models")
def list_models() -> dict[str, list[str]]:
    return {"models": list(_MODELS.keys())}


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
