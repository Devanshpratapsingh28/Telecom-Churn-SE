import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path("artifacts/model_trainer/model.joblib"))
        self.preprocessor = joblib.load(Path("artifacts/data_transformation/preprocessor.pkl"))

    def predict(self, data):
        # Preprocess the input data
        preprocessed_data = self.preprocessor.transform(data)
        prediction = self.model.predict(preprocessed_data)
        return prediction
