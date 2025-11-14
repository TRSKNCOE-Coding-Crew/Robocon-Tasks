from ultralytics import YOLO

# Path to your dataset
DATASET_PATH = r"E:/shreyash1/dataset"

# Load YOLO classification model
model = YOLO("yolov8n-cls.pt")

# Train
model.train(
    data=DATASET_PATH,
    epochs=30,
    imgsz=224,
    project="E:/shreyash1/dataset/runs/classify",
    name="train_script"
)

print("Training complete! Model saved in: runs/classify/train_script/")
