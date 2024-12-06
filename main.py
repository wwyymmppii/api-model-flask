import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Typo diperbaiki di sini
import io
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow import keras
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify

# Load model
model = keras.models.load_model("./model/model.h5")
mlb = MultiLabelBinarizer()

# Define labels
labels = [
    "Backpacks", "Black", "Blue", "Briefs", "Brown", "Caps", "Casual Shoes",
    "Clutches", "Dresses", "Flats", "Flip Flops", "Formal Shoes", "Green", "Grey",
    "Handbags", "Heels", "Innerwear Vests", "Jackets", "Jeans", "Nail Polish", "Navy Blue",
    "Pink", "Purple", "Red", "Sandals", "Shirts", "Shorts", "Silver", "Socks", "Sports Shoes", 
    "Sweaters", "Sweatshirts", "Ties", "Tops", "Track Pants", "Trousers", "Tshirts", "Tunics", "White"
]

# Fit the MultiLabelBinarizer
mlb.fit([labels])  # Ensure fitting is only done once

# Initialize Flask app
app = Flask(__name__)

def predict_label(image_array):
    # Predict probabilities
    predictions = model.predict(image_array)
    # Binarize predictions based on a threshold
    predictions_binarized = (predictions > 0.05).astype(int)
    # Decode binarized predictions
    result = mlb.inverse_transform(predictions_binarized)
    return result

@app.route("/predict", methods=["POST"])
def index():
    file = request.files.get('file')
    if not file or file.filename == "":
        return jsonify({"error": "No file provided"}), 400

    # Read image and preprocess
    img = Image.open(io.BytesIO(file.read()))
    resized_img = img.resize((96, 64), Image.NEAREST)
    image_array = np.array(resized_img, dtype="float32") / 255.0
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Predict and return the result
    result = predict_label(image_array)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))

