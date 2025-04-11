from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Load your Keras model
model = load_model("plant_disease_model.h5")

# Replace with your model's actual classes
# class_names = ['Apple___Black_rot', 'Apple___healthy', 'Corn___Cercospora_leaf_spot', 'Corn___healthy', 'Apple___healthy', 'Corn___Cercospora_leaf_spot', 'Corn___healthy']


class_names = ["Apple_leaf", "Apple_rust_leaf", "Apple_Scab_Leaf", "Bell_pepper_leaf", "Bell_pepper_leaf_spot", "Blueberry_leaf", "Cherry_leaf", "Corn_Gray_leaf_spot", "Corn_leaf_blight", "Corn_rust_leaf", "grape_leaf", "grape_leaf_black_rot", "Peach_leaf", "Potato_leaf_early_blight", "Potato_leaf_late_blight", "Raspberry_leaf", "Soyabean_leaf", "Squash_Powdery_mildew_leaf," "Strawberry_leaf", "Tomato_Early_blight_leaf", "Tomato_leaf", "Tomato_leaf_bacterial_spot," "Tomato_leaf_late_blight", "Tomato_leaf_mosaic_virus", "Tomato_leaf_yellow_virus", "Tomato_mold_leaf", "Tomato_Septoria_leaf_spot", "Tomato_two_spotted_spider_mites_leaf"]

# Image preprocessor
def preprocess_image(image_path, target_size=(224, 224)):
    image = load_img(image_path, target_size=target_size)
    image = img_to_array(image)
    image = image / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)
    return image

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    try:
        image = preprocess_image(filepath)
        predictions = model.predict(image)
        # predicted_class = class_names[np.argmax(predictions[0])]
        index = np.argmax(predictions[0])
        if index >= len(class_names):
            return jsonify({"error": f"Predicted index {index} out of range for {len(class_names)} classes."}), 500

        predicted_class = class_names[index]
        confidence = float(np.max(predictions[0]))

        print("Raw prediction scores:", predictions)
        print("Argmax index:", np.argmax(predictions[0]))

        os.remove(filepath)  # Clean up

        return jsonify({
            "label": predicted_class,
            "confidence": round(confidence * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
