from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# ---------------------------------------------------------
# FIX: Explicitly set the template folder path
# Get the current directory of this script (src/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Point to the 'templates' folder one level up
template_dir = os.path.join(current_dir, '..', 'templates')

application = Flask(__name__, template_folder=template_dir)
# ---------------------------------------------------------

app = application

## Route for a home page
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # CAPTURE DATA
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            # LOGIC FIX: Ensure reading reads reading, writing reads writing
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )
        
        pred_df = data.get_data_as_data_frame()
        print("Received Data for Prediction:")
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        print(f"Prediction Result: {results[0]}")
        
        return render_template('home.html', results=results[0])
    

if __name__ == "__main__":
    port = 5000
    print(f" \n --- STARTING SERVER ---")
    print(f" * Access the app at: http://127.0.0.1:{port}/")
    print(f" * Debug mode is ON")
    print(f" -----------------------\n")
    
    app.run(host="0.0.0.0", port=port, debug=True)