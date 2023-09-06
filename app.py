


# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import ast
import pickle
import os
import pandas as pd
from werkzeug.utils import secure_filename
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import openpyxl
import xlrd
from pathlib import Path
from static.module.utils import numerical_variable

# Create the Flask app instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'

# Define the numerical variables and their ranges
numerical_variable = numerical_variable


def data_processor(data):
    # Function to process the data and make predictions
    result = {0: 'Spruce/Fir',
              1: 'Lodgepole Pine',
              2: 'Ponderosa Pine',
              3: 'Cottonwood/Willow',
              4: 'Aspen',
              5: 'Douglas-fir',
              6: 'Krummholz'}

    pre_processor = pickle.load(
        open(os.path.join('static/modelpara/preprocessor.pkl'), 'rb'))
    model = pickle.load(
        open(os.path.join('static/modelpara/best_model.pkl'), 'rb'))
    output = pre_processor.transform(data)
    output = model.predict_proba(output)

    if len(output) == 1:
        max_indices = np.argmax(output)

        return result[max_indices]
    else:
        output = np.array(output)
        output = np.argmax(output, axis=1)
        forest_type = [result[x] for x in output]

        data['Predicted Class'] = output
        data['Forest Clove Type'] = forest_type

        result_path = Path(os.path.join(app.config['UPLOAD_FOLDER'],'download_data','result.xlsx'))
        data.to_csv(result_path,index=False)
        
        return result_path


def form3_data_parser(form_data):
    # Function to parse the data from the form
    keys = [x[0] for x in form_data.items() if x[0] not in [
        'Wilderness_Area_Type', 'Soil_Type']]
    values = [float(x[1]) for x in form_data.items() if x[0]
              not in ['Wilderness_Area_Type', 'Soil_Type']]

    wildness_index = int(
        [x[1] for x in form_data.items() if x[0] == 'Wilderness_Area_Type'][0])
    soil_index = int([x[1]
                      for x in form_data.items() if x[0] == 'Soil_Type'][0])

    wilderness_keys = [f"Wilderness_Area_{x}" for x in range(4)]
    soil_type_keys = [f"Soil_Type_{x}" for x in range(40)]

    wilderness_values = [0.0]*4
    wilderness_values[wildness_index] = 1.0

    soil_type_values = [0.0]*40
    soil_type_values[soil_index] = 1.0

    combined_keys = keys + wilderness_keys + soil_type_keys
    combined_values = values + wilderness_values + soil_type_values

    data = {x[0]: x[1] for x in zip(combined_keys, combined_values)}

    return data


@app.route('/')
def home():
    # Home route to render the index.html template
    return render_template('index.html',
                           numerical_variable=numerical_variable,
                           )


@app.route('/form1', methods=['POST'])
def form1_submission():
    # Route to handle form1 submission (uploading data file)
    if 'file' in request.files:
        try:
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(app.config['UPLOAD_FOLDER'] + '/uploaded_data/' + filename)

            data = pd.read_excel(
                app.config['UPLOAD_FOLDER'] + '/uploaded_data/' + filename)

            if data.shape[1] == 55:
                data = data.iloc[:, :-1]  # Get all columns except the last one

            # Process the data using the data_processor function
            result = data_processor(data)

            return render_template('thankyou.html', result=result, multiple_value=False)

        except Exception as e:
            print(e)

    # If there is an issue, redirect back to the home page
    return redirect(url_for('home'))


@app.route('/form2', methods=['POST'])
def form2_submission():
    # Route to handle form2 submission (text input)
    if 'text_input' in request.form:
        try:
            input_text = request.form.get('text_input')
            data = ast.literal_eval(input_text)
            data = pd.DataFrame([data])

            # Process the data using the data_processor function
            result = data_processor(data)

            return render_template('thankyou.html', result=result, multiple_value=True)

        except Exception as e:
            print(e)

    # If there is an issue, redirect back to the home page
    return redirect(url_for('home'))


@app.route('/form3', methods=['POST'])
def form3_submission():
    # Route to handle form3 submission (filled form data)
    try:
        form_data = request.form.to_dict()
        data = form3_data_parser(form_data)
        data = pd.DataFrame([data])
        result = data_processor(data)
        return render_template('thankyou.html', result=result, multiple_value=True)

    except Exception as e:
        print(e)
        # If there is an issue, redirect back to the home page
        return redirect(url_for('home'))


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
