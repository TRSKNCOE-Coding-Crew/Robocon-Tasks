# train.py
# Kung Fu Scroll Classifier using YOLOv8 classification

from ultralytics import YOLO
import os

# Paths
DATASET_PATH = "Utkarsh/datasets"   # your dataset folder with train/ and val/
MODEL_SAVE_PATH = "Utkarsh/model/best.pt"  # path to save trained model

# Training parameters
EPOCHS = 30
IMAGE_SIZE = 224
MODEL_NAME = "yolov8s-cls.pt"  # pretrained YOLOv8 classification model

# Check if model folder exists
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# Load YOLOv8 classification model
model = YOLO(MODEL_NAME)

# Train the model
# YOLO automatically detects classes from folder names in train/ and val/
model.train(
    data=DATASET_PATH,   # path to dataset folder
    epochs=EPOCHS,
    imgsz=IMAGE_SIZE,
    save=True
)

# Save the best model manually (optional, YOLO also saves automatically)
model.export(format="pt")
print(f"Training completed. Model saved to {MODEL_SAVE_PATH}")
