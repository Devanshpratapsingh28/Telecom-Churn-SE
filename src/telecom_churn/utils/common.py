import os
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml_file(yaml_file_path: Path) -> ConfigBox:
    """Reads a YAML file and returns its contents as a ConfigBox object."""
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file '{yaml_file_path}' read successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty.")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(paths, verbose=True):
    """Creates directories if they do not exist."""
    for path in paths:
        path = Path(path) 
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves JSON data to a file."""
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logger.info(f"JSON file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads JSON data from a file and returns it as a ConfigBox."""
    with open(path, 'r') as json_file:
        content = json.load(json_file)
    logger.info(f"JSON file loaded from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Saves data to a binary file using joblib."""
    joblib.dump(data, path)
    logger.info(f"Binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads data from a binary file using joblib."""
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data
