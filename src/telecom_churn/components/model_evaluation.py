import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from pathlib import Path
import joblib
import tempfile
from src.telecom_churn import logger 
from src.telecom_churn.entity.config_entity import ModelEvaluationConfig
from src.telecom_churn.utils.common import save_json

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]
        pred_y = model.predict(test_x)
        (rmse, mae, r2) = self.eval_metrics(test_y, pred_y)

        scores = {"rmse": rmse, "mae": mae, "r2": r2}
        save_json(path=Path(self.config.metrics_file_path), data=scores)
