from flask import Flask, render_template, request
import os
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model(r'E:\projects\bone dataset\trained model\bone_detection_model.h5')


# Set the threshold value for classification
threshold = 0.5  # Adjust this threshold as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Save the uploaded image to a temporary file
        temp_filename = 'temp_image.jpg'
        uploaded_file.save(temp_filename)

        # Load and preprocess the image
        img = Image.open(temp_filename)

        # Convert the image to RGB if it has more than 3 channels
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img = img.resize((224, 224))
        img = np.asarray(img)
        img = img / 255.0

        # Perform inference with the loaded model
        prediction = model.predict(np.expand_dims(img, axis=0))

        # Determine the result based on the threshold
        if prediction[0] > threshold:
            result = "Not Fractured"
        else:
            result = "Fractured"

        return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
