from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from werkzeug.utils import secure_filename
import time
from flask import jsonify
import numpy as np
from pandas import Series
import pandas as pd

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_prediction.import_form import ImportForm

# Import module models
from app.mod_exploration.Time import Time

# Define the blueprint
mod_prediction = Blueprint('predict', __name__, url_prefix='/predict')

#----------------
# Standard Routes
#----------------

# Time Series Exploration
@mod_prediction.route('/time', methods=['GET', 'POST'])
def time_series():

    # If importing a file
    import_form = ImportForm(request.form)

    return render_template("prediction/time.html", header="ExpressPredict | Predict", form=import_form)


# Regression Exploration
@mod_prediction.route('/regression', methods=['GET', 'POST'])
def regression():

    # If importing a file
    import_form = ImportForm(request.form)

    return render_template("prediction/regression.html", header="ExpressPredict | Predict", form=import_form)

# Classification
@mod_prediction.route('/classification', methods=['GET', 'POST'])
def classification():

    # If importing a file
    import_form = ImportForm(request.form)

    return render_template("prediction/classification.html", header="ExpressPredict | Predict", form=import_form) 



#--------------------------
# AJAX Controller Functions
#--------------------------

# File Upload
@mod_prediction.route('/uploadTime', methods=['POST'])
def uploadTime():

    cur_time = int(time.time()) 

    if request.method == 'POST':

        if request.files['data_file']:

            file = request.files['data_file']
            filename = secure_filename(file.filename)
            f = filename.split('.')

            file_loc = 'uploads/' + f[0] + '_' + str(cur_time) + '.' + f[1]
            file.save(file_loc)

            # New Time-series model
            ts = Time()

            # Convert raw to DF (x,)
            print("Reading in Dataframe...")
            dataframe = ts.doDataframe(file_loc)
            raw_df = dataframe[0]
            
            print("After import:")
            print(raw_df)
            print(raw_df.shape)

            # Scaled / Stationary
            print("Done... Scaling Data....")
            # standardScaler = ts.doStandardScale(raw_df)
            # df_stand = standardScaler[0]

            print("Done... Normlizing Data....")
            normScaler =ts.doNormalize(raw_df)
            df_norm = normScaler[0]

            print("After Scaling:")
            print(df_norm)
            print(df_norm.shape)

            # Dicky-Fuller test for stationality
            print("Done... Testing for stationality...")
            fuller = ts.doFuller(df_norm.T.squeeze())
            p = fuller[1]

            # We need to keep track of the datasets as they are differenced
            # We will need to use the datasets at each step to 'undifference'
            # the predictions
            diff_series = []
            diff_series.append(df_norm.reshape(1,-1)[0])

            # While the p-value is less than the critical value (0.05)...
            # ...we can reject the null hypothesis
            times_diffd = 0
            index = 1
            if p < 0.05:
                print("Already stationary")
                tmp_df = df_norm.T.squeeze()
            else:
                df_norm = df_norm.T.squeeze()
                while(p > 0.05):
                    print("Not stationary")
                    tmp_df = ts.doStationary(df_norm)
                    tmp_fuller = ts.doFuller(tmp_df)
                    df_norm = tmp_df
                    diff_series.append(tmp_df)
                    p = tmp_fuller[1]
                    times_diffd += 1
                    index += 1

            # If we difference more than two times,
            # this dataset if too random
            if times_diffd > 2:
                return "Error!"

            df_final = pd.DataFrame(tmp_df).to_numpy()

            # print("Times diff'd: ")
            # print(times_diffd)

            # print("Final DF:")
            # print(df_final)
            # print(df_final.shape)

            # If ARIMA Selected
            print("Done... Running Model...")
            if request.form.get('method') == 'arima':
                preds = ts.doARIMA(df_final, request.form.get('num_preds'), times_diffd)
            elif request.form.get('method') == 'ses':
                preds = ts.doSES(df_final, request.form.get('num_preds'))
            elif request.form.get('method') == 'mean':
                preds = ts.doSES(df_final, request.form.get('num_preds'))
            else: pass   

            # print("After Model:")
            # print(preds)  

            # Reverse Differencing 
            if times_diffd > 0:
                preds = ts.doStationaryRevert(diff_series, preds)

            # print("After Scale:")
            # print(df_norm)
            # print(df_norm.shape)

            # Concat preds into original DF
            reverted = np.concatenate((pd.DataFrame(df_norm), pd.DataFrame(preds)), axis=0)
            # print("Before Unscale:")
            # print(reverted)
            # print(reverted.shape)

            # Revert Dataframe to original scale
            final_pred = normScaler[1].inverse_transform(reverted)
            # final_pred = standardScaler[1].inverse_transform(norm_revert)

            print("Revert Scaling:")
            print(final_pred)

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
            response['final'] = final_pred.tolist()
            response['columns'] = dataframe[1]
            response['num_preds'] = int(request.form.get('num_preds'))
            response['raw_mean'] = round(r_mean, 3)
            response['formatted_mean'] = round(f_mean, 3)
            response['raw_std'] = round(r_std, 3)
            response['raw_var'] = round(r_var, 3)
            response['formatted_std'] = round(f_std, 3)
            response['formatted_var'] = round(f_var, 3)
            response['x'] = request.form.get('x')
            response['y'] = request.form.get('y')

        else:
            response = "Please Upload A File!"

    return jsonify(response)

# Save Graphs and Statistics
@mod_prediction.route('/save', methods=['GET', 'POST'])
def save():
    data = ''
    return data

# Export Graphs and Statistics
@mod_prediction.route('/export', methods=['GET', 'POST'])
def export():
    data = ''
    return data
