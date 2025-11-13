# Telecom-Churn-SE
## Deployed Link : [Telecom-Churn-WebApp](https://telecom-churn-se.onrender.com/)
## Workflows--ML Pipeline

1. Data Ingestion
2. Data Validation
3. Data Transformation-- Feature Engineering,Data Preprocessing
4. Model Trainer
5. Model Evaluation

## Workflows

1. Update config.yaml
2. Update schema.yaml
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py


# Steps : 
1. Create venv:
`conda create -p venv python==3.10 -y`
2. Actiavate venv:
`conda activate venv/`
3. Install Dependencies:
`pip install -r requirements.txt`
4. run command to start : 
`python app.py`
5. Hit the URL that will be display in terminal.
6. After hitting URL ,first add /train in it in browser and hit enter.
7. Then come back to previous URL and enter data to predict churn.