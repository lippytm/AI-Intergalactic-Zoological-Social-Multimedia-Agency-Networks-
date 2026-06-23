"""
Computer Vision Toolkit
=======================
Image classification, object detection (YOLO via ultralytics), and
segmentation helpers using PyTorch / torchvision.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
# Image utilities
# ---------------------------------------------------------------------------

def load_image(path: str | Path) -> Any:
    """Load an image as a PIL Image."""
    from PIL import Image  # type: ignore
    return Image.open(path).convert("RGB")


def preprocess_for_inference(image: Any, size: tuple[int, int] = (224, 224)) -> Any:
    """Return a normalised torch tensor ready for a torchvision model."""
    import torch
    from torchvision import transforms  # type: ignore

    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def load_classifier(model_name: str = "resnet50", pretrained: bool = True) -> Any:
    """Load a torchvision classification model."""
    import torch
    from torchvision import models  # type: ignore

    weights = "DEFAULT" if pretrained else None
    model = getattr(models, model_name)(weights=weights)
    model.eval()
    return model


def classify_image(image_path: str | Path, model_name: str = "resnet50") -> list[tuple[str, float]]:
    """Return top-5 ImageNet class predictions for *image_path*."""
    import json
    import urllib.request
    import torch
    from torchvision.models import ResNet50_Weights  # type: ignore

    model = load_classifier(model_name)
    image = load_image(image_path)
    tensor = preprocess_for_inference(image)

    with torch.no_grad():
        logits = model(tensor)
    probs = torch.softmax(logits, dim=1)[0]

    # ImageNet class labels
    labels = ResNet50_Weights.DEFAULT.meta["categories"]
    top5 = torch.topk(probs, 5)
    return [(labels[idx], float(prob)) for idx, prob in zip(top5.indices, top5.values)]


# ---------------------------------------------------------------------------
# Fine-tuning helper
# ---------------------------------------------------------------------------

def fine_tune(
    model: Any,
    train_loader: Any,
    val_loader: Any,
    num_classes: int,
    epochs: int = 10,
    lr: float = 1e-4,
    device: str = "cpu",
) -> Any:
    """Replace the final layer and fine-tune on a custom dataset."""
    import torch
    import torch.nn as nn
    from torch.optim import AdamW
    from torch.optim.lr_scheduler import CosineAnnealingLR

    # Replace final layer
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    model = model.to(device)

    optimiser = AdamW(model.parameters(), lr=lr)
    scheduler = CosineAnnealingLR(optimiser, T_max=epochs)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimiser.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimiser.step()
            total_loss += loss.item()
        scheduler.step()

        # Validation
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                preds = model(images).argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
        logger.info("Epoch %d/%d  loss=%.4f  val_acc=%.4f", epoch+1, epochs, total_loss, correct/total)

    return model


# ---------------------------------------------------------------------------
# Object detection (YOLOv8)
# ---------------------------------------------------------------------------

def detect_objects(image_path: str | Path, conf_threshold: float = 0.4) -> list[dict]:
    """Run YOLOv8n inference. Requires `ultralytics` package."""
    from ultralytics import YOLO  # type: ignore

    model = YOLO("yolov8n.pt")
    results = model(str(image_path), conf=conf_threshold)
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": r.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox_xyxy": box.xyxy[0].tolist(),
            })
    return detections


if __name__ == "__main__":
    logger.info("Computer-vision toolkit loaded.")
    logger.info("Usage: classify_image('image.jpg') or detect_objects('image.jpg')")
