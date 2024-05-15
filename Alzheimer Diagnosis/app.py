from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
model = tf.keras.models.load_model('alzh_model1.h5')

class_names = ['MildDementia', 'ModerateDementia', 'NonDementia', 'VeryMildDementia']

def predict_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    return predicted_class

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file:
            # Create 'uploads' directory if it doesn't exist
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            image_path = "uploads/" + file.filename
            file.save(image_path)
            predicted_class = predict_image(image_path)
            return render_template('index.html', prediction=predicted_class, image_path=image_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
