from ultralytics import YOLO

# Path to trained model
MODEL_PATH = r"E:/shreyash1/dataset/runs/classify/train2/weights/best.pt"

# Load model
model = YOLO(MODEL_PATH)

# Source file or folder
SOURCE = r"E:/shreyash1/dataset/test.jpg"  # change to your input

model.predict(
    source=SOURCE,
    save=True,
    imgsz=224
)

print("Prediction complete! Check: runs/classify/predict/")
