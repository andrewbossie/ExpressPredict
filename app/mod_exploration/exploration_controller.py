from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from werkzeug.utils import secure_filename
import time
from flask import jsonify
import numpy as np
import pandas as pd

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_exploration.import_form import ImportForm

# Import module models
from app.mod_exploration.Time import Time

# Define the blueprint
mod_explore = Blueprint('explore', __name__, url_prefix='/explore')

#----------------
# Standard Routes
#----------------

# Time Series Exploration
@mod_explore.route('/time', methods=['GET', 'POST'])
def time_series():

    # If importing a file
    import_form = ImportForm(request.form)

    return render_template("exploration/time.html", header="ExpressPredict | Explore", form=import_form)


# Regression Exploration
@mod_explore.route('/regression', methods=['GET', 'POST'])
def regression():

    # If importing a file
    import_form = ImportForm(request.form)

    return render_template("exploration/regression.html", header="ExpressPredict | Explore", form=import_form)

# Classification
@mod_explore.route('/classification', methods=['GET', 'POST'])
def classification():

    # If importing a file
    import_form = ImportForm(request.form)

    return render_template("exploration/classification.html", header="ExpressPredict | Explore", form=import_form) 



#--------------------------
# AJAX Controller Functions
#--------------------------

# File Upload
@mod_explore.route('/upload', methods=['POST'])
def upload():

    cur_time = int(time.time()) 

    if request.method == 'POST':

        file = request.files['data_file']
        filename = secure_filename(file.filename)
        f = filename.split('.')

        file_loc = 'uploads/' + f[0] + '_' + str(cur_time) + '.' + f[1]
        file.save(file_loc)

        # New Time-series model
        ts = Time()

        # Convert raw to DF
        print("Reading in Dataframe...")
        dataframe = ts.doDataframe(file_loc)
        raw_df = dataframe[0]

        # Raw Rolling Mean
        raw_rolling = ts.doRollingMean(raw_df)

        # To-Do Autocorrelation Plots

        # Scaled / Stationary
        print("Done... Scaling Data....")
        standardScaler = ts.doStandardScale(raw_df)
        df_stand = standardScaler[0]

        print("Done... Normlizing Data....")
        normScaler =ts.doNormalize(df_stand)
        df_norm = normScaler[0]

        # Dicky-Fuller test for stationality
        print("Done... Testing for stationality...")
        fuller = ts.doFuller(df_norm.T.squeeze())
        p = fuller[1]

        # While the p-value is less than the critical value...
        # ...we can reject the null hypothesis
        times_diffd = 0
        if p < 0.05:
            tmp_df = df_norm.T.squeeze()
            final_fuller = fuller
        else:
            while(p > 0.05):
                tmp_df = ts.doStationary(df_norm.T.squeeze())
                tmp_fuller = ts.doFuller(tmp_df)
                df_norm = tmp_df
                p = tmp_fuller[1]
                times_diffd += 1
                final_fuller = tmp_fuller

        df_final = pd.DataFrame(tmp_df).to_numpy()

        # Final Rolling Mean
        final_rolling = ts.doRollingMean(df_final)

        # Simple Statistics
        r_mean = ts.doMean(raw_df)
        r_std = ts.doSTD(raw_df)
        r_var = ts.doVar(raw_df)
        f_mean = ts.doMean(df_final)
        f_std = ts.doSTD(df_final)
        f_var = ts.doVar(df_final)

        # Send back
        response = {}
        response['raw'] = raw_df.values.tolist()
        response['formatted'] = df_final.tolist()
        response['columns'] = dataframe[1]
        response['raw_mean'] = round(r_mean, 3)
        response['formatted_mean'] = round(f_mean, 3)
        response['raw_std'] = round(r_std, 3)
        response['raw_var'] = round(r_var, 3)
        response['formatted_std'] = round(f_std, 3)
        response['formatted_var'] = round(f_var, 3)
        response['raw_rolling'] = raw_rolling.transpose().values.tolist()
        response['final_rolling'] = final_rolling.transpose().values.tolist()
        response['fuller'] = final_fuller
        response['x'] = request.form.get('x')
        response['y'] = request.form.get('y')

    return jsonify(response)

# Save Graphs and Statistics
@mod_explore.route('/save', methods=['GET', 'POST'])
def save():
    data = ''
    return data

# Export Graphs and Statistics
@mod_explore.route('/export', methods=['GET', 'POST'])
def export():
    data = ''
    return data
