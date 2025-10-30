import shutil 
from pathlib import Path
from src.telecom_churn import logger  
import urllib as request
from src.telecom_churn.utils.common import create_directories
from src.telecom_churn.entity.config_entity import DataIngestionConfig

# Data-Ingestion Component
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        logger.info("Starting data ingestion process...")

        create_directories([self.config.root_dir])
        destination = Path(self.config.local_data_file)

        try:
            # If already a file exists at destination then skip
            if destination.exists():
                logger.info(f"File already exists at {destination}, skipping download.")
                return
            else :
                # Check if source is a URL or local path
                if self.config.source_URL.startswith(('http://', 'https://')):
                    filename, headers = request.urlretrieve(self.config.source_URL, str(destination))
                    logger.info(f"Downloaded file from {self.config.source_URL} → {destination}")
                else:
                    # Handle local file copy
                    source = Path(self.config.source_URL)
                    if source.exists():
                        shutil.copy(source, destination)
                        logger.info(f"Copied local file from {source} → {destination}")
                    else:
                        raise FileNotFoundError(f"Source file {source} does not exist")

        except Exception as e:
            logger.error(f"Error during data ingestion: {e}")
            raise e
