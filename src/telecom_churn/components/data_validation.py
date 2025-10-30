import pandas as pd
from pathlib import Path
from src.telecom_churn import logger 
from src.telecom_churn.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        """
        Validate if all columns in schema are present and have correct data types
        """
        try:
            validation_status = True
            df = pd.read_csv(self.config.local_data_file)

            all_cols = df.columns.tolist()

            for col in self.config.all_schema.keys():
                if col not in all_cols:
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write("Status:False")
                    logger.error(f"Column: '{col}' is missing from the dataframe. Status: Failed\n")
                    break

                elif str(df[col].dtype) != str(self.config.all_schema[col]):
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write("Status:False")
                    logger.error(f"Column: '{col}' has datatype mismatch. Expected: {self.config.all_schema[col]}, Found: {df[col].dtype}. Status: Failed\n")    
                    break
            else:
                with open(self.config.STATUS_FILE, "w") as f:
                    f.write("Status:True")
                logger.info("Given Data is Valid as per schema.")    

            return validation_status

        except Exception as e:
            logger.error(f"Error during data validation: {e}")
            raise e
