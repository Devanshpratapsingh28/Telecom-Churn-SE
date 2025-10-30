from flask import Flask, render_template, request
import os
import numpy as np
from src.telecom_churn.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html', results=None)

@app.route('/train', methods=['GET'])
def training():
    os.system("python main.py")
    return "Training Successful!"

@app.route('/predict_datapoint', methods=['POST', 'GET'])
def predict_datapoint():
    if request.method == 'POST':
        try:
            AccountWeeks = float(request.form['AccountWeeks'])
            ContractRenewal = int(request.form['ContractRenewal'])
            DataUsage = float(request.form['DataUsage'])
            CustServCalls = int(request.form['CustServCalls'])
            DayMins = float(request.form['DayMins'])
            DayCalls = int(request.form['DayCalls'])
            MonthlyCharge = float(request.form['MonthlyCharge'])
            OverageFee = float(request.form['OverageFee'])
            RoamMins = float(request.form['RoamMins'])

            data = np.array([AccountWeeks, ContractRenewal, DataUsage, CustServCalls,
                             DayMins, DayCalls, MonthlyCharge, OverageFee, RoamMins]).reshape(1, -1)
            obj = PredictionPipeline()
            prediction = obj.predict(data)
            return render_template('index.html', results=int(prediction[0]))
        except Exception as e:
            return render_template('index.html', error="Error during prediction. Please check inputs.")
    return render_template('index.html', results=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
