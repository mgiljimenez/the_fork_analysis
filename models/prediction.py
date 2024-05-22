import joblib
import numpy as np
import pandas as pd

# Función para cargar el modelo y predecir
def load_model_and_predict2(input_data):
    # Carga el modelo desde el archivo pkl
    loaded_model = joblib.load('xgboost_model.pkl')
    
    # Realiza la predicción
    prediction = loaded_model.predict(input_data)
    return prediction

def load_model_and_predict1(input_data):
    # Carga el modelo desde el archivo pkl
    loaded_model = joblib.load('random_forest_model.pkl')
    
    # Realiza la predicción
    prediction = loaded_model.predict(input_data)
    return prediction

def load_model_and_predict3(input_data):
    # Carga el modelo desde el archivo pkl
    loaded_model = joblib.load('linear_regression_model.pkl')
    
    # Realiza la predicción
    prediction = loaded_model.predict(input_data)
    return prediction

def predict_general(input_data):
    p1=load_model_and_predict1(input_data)[0]
    p2=load_model_and_predict2(input_data)[0]
    p3=load_model_and_predict3(input_data)[0]
    return np.mean([p1,p2,p3])