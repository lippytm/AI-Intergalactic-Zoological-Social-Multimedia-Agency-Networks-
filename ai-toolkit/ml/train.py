"""
Machine Learning Training Pipeline
====================================
Covers classical ML (scikit-learn) and gradient-boosting models.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

MODELS: dict[str, Any] = {
    "logistic_regression": LogisticRegression(max_iter=1000),
    "random_forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "gradient_boosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
    "svm": SVC(probability=True, kernel="rbf"),
}


def build_pipeline(model_name: str) -> Pipeline:
    """Wrap a scikit-learn estimator in a scaling pipeline."""
    if model_name not in MODELS:
        raise ValueError(f"Unknown model {model_name!r}. Choose from: {list(MODELS)}")
    return Pipeline([("scaler", StandardScaler()), ("clf", MODELS[model_name])])


def train(
    X_train: np.ndarray,
    y_train: np.ndarray,
    model_name: str = "random_forest",
) -> Pipeline:
    pipe = build_pipeline(model_name)
    logger.info("Training %s on %d samples …", model_name, len(X_train))
    pipe.fit(X_train, y_train)
    cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
    logger.info("CV accuracy: %.3f ± %.3f", cv_scores.mean(), cv_scores.std())
    return pipe


def evaluate(
    pipe: Pipeline,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, float]:
    preds = pipe.predict(X_test)
    proba = pipe.predict_proba(X_test)
    report = classification_report(y_test, preds, output_dict=True)
    try:
        auc = roc_auc_score(y_test, proba, multi_class="ovr")
    except ValueError:
        auc = float("nan")
    logger.info("\n%s", classification_report(y_test, preds))
    logger.info("ROC-AUC: %.4f", auc)
    return {"accuracy": report["accuracy"], "roc_auc": auc}


if __name__ == "__main__":
    from sklearn.datasets import load_iris

    data = load_iris(as_frame=True)
    X, y = data.data.values, data.target.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for name in MODELS:
        pipe = train(X_train, y_train, model_name=name)
        metrics = evaluate(pipe, X_test, y_test)
        logger.info("%s → %s", name, metrics)
