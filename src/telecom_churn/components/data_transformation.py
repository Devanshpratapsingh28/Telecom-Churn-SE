import os
import numpy as np
import joblib
import pandas as pd
from src.telecom_churn import logger
from src.telecom_churn.entity.config_entity import DataTransformationConfig
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, make_column_selector


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_split(self):
        
        # read data
        df = pd.read_csv(self.config.data_path)

        for col in ['Churn', 'ContractRenewal']:
            if col in df.columns:
                try:
                    df[col] = df[col].astype('category')
                except Exception:
                    pass


        if 'Churn' not in df.columns:
            raise Exception("Target column 'Churn' not found in data")

        X = df.drop(columns=['Churn'])
        y = df['Churn']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        num_pipeline = make_pipeline(StandardScaler())
        cat_pipeline = make_pipeline(OneHotEncoder(handle_unknown='ignore'))

        preprocessing = make_column_transformer(
            (num_pipeline, make_column_selector(dtype_include=np.number)),
            (cat_pipeline, make_column_selector(dtype_include='category')),
            remainder='drop'
        )

        X_train_pre = preprocessing.fit_transform(X_train)
        X_test_pre = preprocessing.transform(X_test)

        try:
            feature_names = preprocessing.get_feature_names_out(input_features=X_train.columns)
        except Exception:
            num_cols = list(X_train.select_dtypes(include=np.number).columns)
            cat_cols = list(X_train.select_dtypes(include='category').columns)
            feature_names = []
            feature_names.extend(num_cols)
            for c in cat_cols:
                feature_names.append(f"ohe__{c}")

        try:
            df_train_pre = pd.DataFrame(X_train_pre, columns=feature_names)
            df_test_pre = pd.DataFrame(X_test_pre, columns=feature_names)
        except Exception:
            df_train_pre = pd.DataFrame(X_train_pre)
            df_test_pre = pd.DataFrame(X_test_pre)

        df_train_pre.reset_index(drop=True, inplace=True)
        df_test_pre.reset_index(drop=True, inplace=True)
        df_train_pre['Churn'] = y_train.reset_index(drop=True)
        df_test_pre['Churn'] = y_test.reset_index(drop=True)

        os.makedirs(self.config.root_dir, exist_ok=True)
        train_path = os.path.join(self.config.root_dir, "train.csv")
        test_path = os.path.join(self.config.root_dir, "test.csv")
        preprocessor_path = os.path.join(self.config.root_dir, "preprocessor.pkl")

        df_train_pre.to_csv(train_path, index=False)
        df_test_pre.to_csv(test_path, index=False)
        joblib.dump(preprocessing, preprocessor_path)

        logger.info("Train and test split and preprocessing completed (80:20).")
        logger.info(f"Train Shape : {df_train_pre.shape} and Test Shape : {df_test_pre.shape}")

        print(
            "Train and test split is done successfully in ratio 80:20.\n"
            f"Train Shape: {df_train_pre.shape} and Test Shape: {df_test_pre.shape}"
        )