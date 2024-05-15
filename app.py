from flask import Flask, render_template, request , jsonify
import pickle
import numpy as np
import pandas as pd
import pyodbc
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os


app = Flask(__name__)

# Load the diabetes prediction model
diabetes_model = pickle.load(open('diabetes.pkl', 'rb'))

# Load the breast cancer prediction model
breast_cancer_model = pickle.load(open('breast_cancer.pkl', 'rb'))

# Load the hepatitis prediction model
hepatitis_model = pickle.load(open('hepatitis_c.pkl', 'rb'))

# Load the Alzheimer's prediction model
alzheimer_model = tf.keras.models.load_model('alzh_model1.h5')
alzheimer_class_names = ['MildDementia', 'ModerateDementia', 'NonDementia', 'VeryMildDementia']

# Feature names for breast cancer prediction
breast_cancer_feature_names = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
                               'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
                               'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
                               'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
                               'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
                               'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst',
                               'symmetry_worst', 'fractal_dimension_worst']

# Feature names for hepatitis prediction
hepatitis_feature_names = ['Age', 'Sex', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE', 'CHOL', 'CREA', 'GGT', 'PROT']

# Establish connection to SQL Server for diabetes prediction
diabetes_conn = pyodbc.connect('DRIVER={SQL Server};' 'SERVER=Mohamed-Alaa1;' 'DATABASE=Diabetes Predictions;' 'Trusted_Connection=yes;')

# Establish connection to SQL Server for breast cancer prediction
breast_cancer_conn = pyodbc.connect('DRIVER={SQL Server};' 'SERVER=Mohamed-Alaa1;' 'DATABASE=Breast Cancer Predictions;' 'Trusted_Connection=yes;')

# Establish connection to SQL Server for hepatitis prediction
hepatitis_conn = pyodbc.connect('DRIVER={SQL Server};' 'SERVER=Mohamed-Alaa1;' 'DATABASE=prediction;' 'Trusted_Connection=yes;')

def predict_image(image_path):
    model = tf.keras.models.load_model('alzh_model1.h5')
    class_names = ['MildDementia', 'ModerateDementia', 'NonDementia', 'VeryMildDementia']
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    return predicted_class

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    if request.method == 'POST':
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        blood_pressure = float(request.form['blood_pressure'])
        skin_thickness = float(request.form['skin_thickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        diabetes_pedigree_function = float(request.form['diabetes_pedigree_function'])
        age = float(request.form['age'])

        # Perform prediction using your model
        prediction_data = np.array([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]).reshape(1, -1)
        prediction = diabetes_model.predict(prediction_data)

        if prediction:
            result = 'you have diabetes, visit your doctor as soon as possible'
        else:
            result = 'good news , you do not have diabetes'

        cursor = diabetes_conn.cursor()
        cursor.execute("INSERT INTO DiabetesPredictions (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Prediction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age, result))
        diabetes_conn.commit()

        return jsonify({'result': result})

@app.route('/predict_breast_cancer', methods=['POST'])
def predict_breast_cancer():
    if request.method == 'POST':
        data = request.form.to_dict()
        new_data = np.array(list(data.values()), dtype=float).reshape(1, -1)
        new_data_df = pd.DataFrame(data=new_data, columns=breast_cancer_feature_names)

        prediction = breast_cancer_model.predict(new_data_df)

        if prediction == 0:
            prediction_text = "Good news, You do not have breast cancer."
        elif prediction == 1:
            prediction_text = "Unfortunately, you have Breast Cancer. Visit the doctor as soon as possible."
        else:
            prediction_text = "Error 404"

        cursor = breast_cancer_conn.cursor()
        values = [prediction_text] + new_data.tolist()[0]
        cursor.execute('''INSERT INTO predictions (Prediction, radius_mean, texture_mean, perimeter_mean, area_mean,
                        smoothness_mean, compactness_mean, concavity_mean,
                        concave_points_mean, symmetry_mean, fractal_dimension_mean,
                        radius_se, texture_se, perimeter_se, area_se, smoothness_se,
                        compactness_se, concavity_se, concave_points_se, symmetry_se,
                        fractal_dimension_se, radius_worst, texture_worst,
                        perimeter_worst, area_worst, smoothness_worst,
                        compactness_worst, concavity_worst, concave_points_worst,
                        symmetry_worst, fractal_dimension_worst)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
        breast_cancer_conn.commit()

        return jsonify({'result': prediction_text})

@app.route('/predict_hepatitis', methods=['POST'])
def predict_hepatitis():
    if request.method == 'POST':
        input_data = [float(x) for x in request.form.values()]
        new_data = np.array(input_data).reshape(1, -1)
        new_data_df = pd.DataFrame(data=new_data, columns=hepatitis_feature_names)

        prediction = hepatitis_model.predict(new_data_df)

        if prediction == 0:
            prediction_text = "You are not sick."
        elif prediction == 1:
            prediction_text = "Unfortunately, you have Hepatitis."
        elif prediction == 2:
            prediction_text = "Unfortunately, you have Fibrosis."
        elif prediction == 3:
            prediction_text = "Unfortunately, you have Cirrhosis."
        else:
            prediction_text = "Error 404"

        cursor = hepatitis_conn.cursor()
        cursor.execute('''INSERT INTO predictions (Prediction, Age, Sex, ALB, ALP, ALT, AST, BIL, CHE, CHOL, CREA, GGT, PROT)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       [prediction_text] + input_data)
        hepatitis_conn.commit()

        return jsonify({'result': prediction_text})

@app.route('/predict_alzheimer', methods=['POST'])
def predict_alzheimer():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            image_path = "uploads/" + file.filename
            file.save(image_path)
            predicted_class = predict_image(image_path)
            return jsonify({'result': predicted_class})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
