"""
Data Pipeline
=============
End-to-end data ingestion, cleaning, transformation, and feature engineering.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------

def load_csv(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    df = pd.read_csv(path, **kwargs)
    logger.info("Loaded %d rows × %d cols from %s", *df.shape, path)
    return df


def load_json(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    """Load a JSON file into a DataFrame."""
    df = pd.read_json(path, **kwargs)
    logger.info("Loaded %d rows × %d cols from %s", *df.shape, path)
    return df


# ---------------------------------------------------------------------------
# Cleaning
# ---------------------------------------------------------------------------

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    logger.info("Dropped %d duplicate rows", before - len(df))
    return df


def fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Fill missing numeric values using *strategy* ('mean', 'median', 'zero')."""
    numeric = df.select_dtypes(include="number").columns
    if strategy == "mean":
        df[numeric] = df[numeric].fillna(df[numeric].mean())
    elif strategy == "median":
        df[numeric] = df[numeric].fillna(df[numeric].median())
    elif strategy == "zero":
        df[numeric] = df[numeric].fillna(0)
    else:
        raise ValueError(f"Unknown strategy: {strategy!r}")
    return df


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------

def encode_labels(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Label-encode categorical columns in place."""
    le = LabelEncoder()
    for col in columns:
        df[col] = le.fit_transform(df[col].astype(str))
    return df


def scale_features(
    df: pd.DataFrame,
    columns: list[str],
    method: str = "standard",
) -> tuple[pd.DataFrame, Any]:
    """Scale numeric columns. Returns (df, scaler)."""
    scaler = StandardScaler() if method == "standard" else MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------

def split_data(
    df: pd.DataFrame,
    target: str,
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split DataFrame into train / validation / test sets."""
    X = df.drop(columns=[target])
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=val_size / (1 - test_size), random_state=random_state
    )
    logger.info(
        "Split sizes — train: %d, val: %d, test: %d",
        len(X_train), len(X_val), len(X_test),
    )
    train_df = X_train.copy(); train_df[target] = y_train
    val_df   = X_val.copy();   val_df[target]   = y_val
    test_df  = X_test.copy();  test_df[target]  = y_test
    return train_df, val_df, test_df


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(source: str | Path, target_col: str) -> None:
    """Demonstrate a full pipeline run on *source* CSV."""
    df = load_csv(source)
    df = drop_duplicates(df)
    df = fill_missing(df, strategy="mean")
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    if cat_cols:
        df = encode_labels(df, cat_cols)
    num_cols = [c for c in df.select_dtypes(include="number").columns if c != target_col]
    df, _ = scale_features(df, num_cols)
    train, val, test = split_data(df, target=target_col)
    logger.info("Pipeline complete. train=%d val=%d test=%d", len(train), len(val), len(test))


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        run_pipeline(sys.argv[1], sys.argv[2])
    else:
        # Demo with synthetic data
        rng = np.random.default_rng(0)
        demo = pd.DataFrame({
            "feature_a": rng.normal(size=1000),
            "feature_b": rng.normal(size=1000),
            "category":  rng.choice(["cat", "dog", "bird"], size=1000),
            "label":     rng.integers(0, 2, size=1000),
        })
        demo.to_csv("/tmp/demo_data.csv", index=False)
        run_pipeline("/tmp/demo_data.csv", "label")
