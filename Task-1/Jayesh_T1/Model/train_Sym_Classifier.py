import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# === LOAD PROCESSED DATA ===
dataset_dir = "processed_dataset"

classes = ["R1_real", "R2_real", "R2_fake"]  # Three classes
X, y = [], []

for idx, cls in enumerate(classes):
    folder = os.path.join(dataset_dir, cls)
    for file in os.listdir(folder):
        if file.endswith(".npy"):
            data = np.load(os.path.join(folder, file))
            X.append(data)
            y.append(idx)

X = np.array(X)
y = np.array(y)

print(f"✅ Loaded {len(X)} images from {len(classes)} classes.")

# === SPLIT INTO TRAIN & TEST ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📚 Training: {len(X_train)}, Testing: {len(X_test)}")

# === DEFINE CNN MODEL ===
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(len(classes), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# === TRAIN MODEL ===
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=8,
    validation_data=(X_test, y_test)
)

# === EVALUATION ===
y_pred = np.argmax(model.predict(X_test), axis=1)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=classes))

cm = confusion_matrix(y_test, y_pred)
plt.imshow(cm, cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

# === SAVE MODEL ===
model.save("scroll_classifier_model.h5")
print("\n💾 Model saved as scroll_classifier_model.h5")
