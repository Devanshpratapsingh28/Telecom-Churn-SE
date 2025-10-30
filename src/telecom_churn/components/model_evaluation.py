import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path
import joblib
from src.telecom_churn import logger 
from src.telecom_churn.entity.config_entity import ModelEvaluationConfig
from src.telecom_churn.utils.common import save_json

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred, average='weighted')
        recall = recall_score(actual, pred, average='weighted')
        f1 = f1_score(actual, pred, average='weighted')
        return accuracy, precision, recall, f1

    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[self.config.target_column]
        model = joblib.load(self.config.model_path)
        pred_y = model.predict(test_x)
        (accuracy, precision, recall, f1) = self.eval_metrics(test_y, pred_y)

        scores = {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1)
        }
        save_json(path=Path(self.config.metrics_file_path), data=scores)
