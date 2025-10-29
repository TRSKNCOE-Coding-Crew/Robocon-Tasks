import cv2
import os
import numpy as np

# INPUT FILES
r2_real_path = "R2_Real.jpg"
r2_fake_path = "R2_Fake.jpg"
r1_red_path = "R1_Real_RED.jpg"
r1_blue_path = "R1_Real_BLUE.jpg"

# OUTPUT FOLDERS
raw_dir = "dataset"
processed_dir = "processed_dataset"

os.makedirs(f"{raw_dir}/R2_real", exist_ok=True)
os.makedirs(f"{raw_dir}/R2_fake", exist_ok=True)
os.makedirs(f"{raw_dir}/R1_real", exist_ok=True)

os.makedirs(f"{processed_dir}/R2_real", exist_ok=True)
os.makedirs(f"{processed_dir}/R2_fake", exist_ok=True)
os.makedirs(f"{processed_dir}/R1_real", exist_ok=True)


# FUNCTION TO SPLIT GRID IMAGES
def split_grid(image_path, rows, cols, label_folder, prefix):
    img = cv2.imread(image_path)
    if img is None:
        print(f"⚠️ Could not read {image_path}")
        return
    h, w, _ = img.shape
    cell_h, cell_w = h // rows, w // cols
    count = 1
    for i in range(rows):
        for j in range(cols):
            y1, y2 = i * cell_h, (i + 1) * cell_h
            x1, x2 = j * cell_w, (j + 1) * cell_w
            crop = img[y1:y2, x1:x2]
            filename = f"{prefix}_{count:02d}.jpg"
            save_path = os.path.join(label_folder, filename)
            cv2.imwrite(save_path, crop)
            count += 1
    print(f"✅ Cropped {count-1} images from {image_path} into {label_folder}")


# 1. SPLIT R2 REAL & FAKE
split_grid(r2_real_path, 3, 5, f"{raw_dir}/R2_real", "r2_real")
split_grid(r2_fake_path, 3, 5, f"{raw_dir}/R2_fake", "r2_fake")

# 2. COPY R1 REAL SYMBOLS
for idx, path in enumerate([r1_red_path, r1_blue_path]):
    img = cv2.imread(path)
    if img is not None:
        save_path = os.path.join(f"{raw_dir}/R1_real", f"r1_real_{idx+1}.jpg")
        cv2.imwrite(save_path, img)
print("✅ Copied R1 real images.")

# 3. RESIZE & NORMALIZE
TARGET_SIZE = (128, 128)  # pixels


def process_and_save_images(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        path = os.path.join(input_folder, file_name)
        img = cv2.imread(path)
        if img is not None:
            resized = cv2.resize(img, TARGET_SIZE)
            norm = resized.astype(np.float32) / 255.0  # Normalize 0–1
            # Save normalized image as .npy array for model loading later
            base_name = os.path.splitext(file_name)[0]
            np.save(os.path.join(output_folder, base_name + ".npy"), norm)
    print(f"✅ Processed images from {input_folder} → {output_folder}")


# Apply preprocessing to all folders
for folder in ["R2_real", "R2_fake", "R1_real"]:
    process_and_save_images(f"{raw_dir}/{folder}", f"{processed_dir}/{folder}")

print(
    "\n🎉 All images cropped, resized to 128×128, normalized (0–1), and saved to ./processed_dataset/"
)
