import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path

@dataclass
class DataValidationConfig:
    root_dir: Path
    local_data_file: Path
    STATUS_FILE: str
    all_schema : dict 

@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path : Path 
    preprocessor_path: Path 

@dataclass
class ModelTrainerConfig :
    root_dir : Path
    train_data_path : Path
    test_data_path : Path
    model_name : str
    random_state : int
    min_samples_split : int
    target_column : str

@dataclass
class ModelEvaluationConfig:
    root_dir : Path
    test_data_path : Path
    model_path : Path
    all_params : dict
    metrics_file_path : Path
    target_column : str      