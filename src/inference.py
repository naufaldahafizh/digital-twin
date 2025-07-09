import joblib
import pandas as pd

def load_model(path):
    model = joblib.load(path)
    return model

def predict(model, input_df):
    return model.predict(input_df), model.predict_proba(input_df)
