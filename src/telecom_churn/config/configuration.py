from pathlib import Path
from src.telecom_churn.constants import *
from src.telecom_churn.utils.common import read_yaml_file, create_directories
from src.telecom_churn.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig

class ConfigManager:
    def __init__(self,
                 config_file_path=CONFIG_FILE_PATH,
                 params_file_path=PARAMS_FILE_PATH,
                 schema_file_path=SCHEMA_FILE_PATH):
        self.config = read_yaml_file(config_file_path)
        self.params = read_yaml_file(params_file_path)
        self.schema = read_yaml_file(schema_file_path)

        create_directories([Path(self.config['artifacts-root'])])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config['data_ingestion']

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_URL=config.source_URL,  # keep str
            local_data_file=Path(config.local_data_file)
        )

        # create directories using Path objects
        create_directories([data_ingestion_config.root_dir])

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config['data_validation']
        schema = self.schema['COLUMNS']

        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            local_data_file=Path(config.local_data_file),
            STATUS_FILE=config.STATUS_FILE,
            all_schema = schema
        )

        # create directories using Path objects
        create_directories([data_validation_config.root_dir])

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config['data_transformation']
        create_directories([config.root_dir]) # Here we are putting root dir inside a list because our create_directories function accepts a list of paths
        data_transformation_config = DataTransformationConfig(
            root_dir = config.root_dir,
            data_path=config.data_path,
            preprocessor_path=config.preprocessor_path
        )
        return data_transformation_config 

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config['model_trainer']
        params = self.params['RandomForest']
        tar_col = self.schema['TARGET_COLUMN']['name']
        create_directories([config.root_dir])
        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            model_name = config.model_name,
            random_state = params.random_state,
            min_samples_split = params.min_samples_split,
            target_column = tar_col
        )
        return model_trainer_config 

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config['model_evaluation']
        params = self.params['RandomForest']
        target_col = self.schema['TARGET_COLUMN']['name']

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=Path(config.root_dir),
            test_data_path=Path(config.test_data_path),
            model_path=Path(config.model_path),
            all_params=params,
            metrics_file_path=Path(config.metrics_file_path),
            target_column=target_col
        )
        return model_evaluation_config 
