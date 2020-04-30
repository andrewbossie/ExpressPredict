from app import db
import matplotlib as plt
import numpy as np
import pandas as pd 
import statsmodels
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.tools import diff
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARMAResults 
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing, Holt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

class Time(db.Model):

    
    __tablename__ = 'time_models'

    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column('user', db.String(50))

    #----------------
    # Standard Functions
    #----------------

    def doDataframe(self, filename):

        f = filename.split('.')
        ext = f[1]

        # Peek at file to determine dimensions
        if ext.lower() == "csv":
            tmp = pd.read_csv(filename)
        else:
            tmp = pd.read_excel(filename)


        # Row Based
        if len(tmp.columns) > 2:
            # Parse file
            if ext.lower() == "csv":
                df = pd.read_csv(filename)
            else:
                df = pd.read_excel(filename)

        # Else if the data comes in as a column vector
        else:
            # Parse file
            if ext.lower() == "csv":
                df = pd.read_csv(filename, index_col=0, header=None, squeeze=True)
                df = pd.DataFrame(df)
            else:
                df = pd.read_excel(filename)

        # If multiple Rows. Flatten / sum row data
        if len(df.columns) > 2:
            df_formatted = pd.DataFrame(df.sum(axis=0))
            df_formatted = df_formatted[0]
            columns = list(df.columns)
        else:
            df_formatted = df.squeeze()
            columns = df_formatted.index.values.tolist()

        # Return (x,) DataFrame and columns list
        return [pd.DataFrame(df_formatted), columns]

    # Rolling Mean for Trend Line
    def doRollingMean(self, dataframe):
        tmp = pd.DataFrame(dataframe)
        df_rolled = tmp.rolling(2, min_periods=1).mean()
        return df_rolled

    # Scale Data
    def doStandardScale(self, dataframe):
        scaler = StandardScaler()
        scaled = scaler.fit_transform(dataframe)
        return [scaled, scaler]
        
    # Regularize
    def doNormalize(self, dataframe):
        minScaler = MinMaxScaler()
        minMax = minScaler.fit_transform(dataframe)
        return [minMax, minScaler]

     # Make Stationary
    def doStationary(self, dataframe):
        stationary = diff(dataframe)
        return stationary

    # Loop through the data and reverse the differending
    def doStationaryRevert(self, original_dfs, predictions ):

        tmp_df = []
        final_df = []
        j = 0

        # For Each Time Differenced
        for i in range(len(original_dfs[1:])):
            # print(i)

            start_val = original_dfs[j - 1][-1]
            # print(start_val)
            j = j + 1
            # exit()
                
            # Loop through the predictions
            for k in predictions:
                val = start_val + k
                tmp_df.append(val)
                start_val = k

        final_preds = tmp_df

        return final_preds

    def doMean(self, dataframe):
        return dataframe.mean()

    def doSTD(self, dataframe):
        return dataframe.std()

    def doVar(self, dataframe):
            return dataframe.var()

    # Dicky-Fuller Analysis
    def doFuller(self, dataframe):
        adfTest = adfuller(dataframe)
        return adfTest

    def doARIMA(self, dataframe, num_pred, diff):

        # dataframe = dataframe.transpose()

        # Grid Search Params
        # p_grid = [0,1,2,4,6,8]
        # q_grid = [0,1,2,3, 4]
        p_grid = [0,1,2]
        q_grid = [0,1,2]
        completed = {}

        models_tested = 0
        for p in p_grid:
            for q in q_grid:
                    print("p: {}").format(p)
                    print("q: {}").format(q)
                    try:
                        # Build
                        model = ARIMA(dataframe, order=(p,diff,q))
                        model_fit = model.fit()

                        # Evaluate AIC
                        aic = model_fit.aic

                        # store
                        completed[aic] = (p, diff, q)

                        models_tested += 1
                    except Exception as e:
                        print(e)
                        pass

        m = max(completed, key=completed.get)

        # Predict Based on 'Best' Models
        final_model = ARIMA(dataframe, order=(completed[m]))
        final_fit = final_model.fit()
        y_hat = final_fit.predict(len(dataframe), len(dataframe) + int(num_pred))

        # Return Preds
        results = y_hat

        # Predict
        return results

    def doARMA(self, dataframe, num_pred):

        # dataframe = dataframe.transpose()

        # Grid Search Params
        # p_grid = [0,1,2,4,6,8]
        # q_grid = [0,1,2,3, 4]
        p_grid = [0,1,2]
        q_grid = [0,1,2]
        completed = {}

        models_tested = 0
        for p in p_grid:
            for q in q_grid:
                    print("p: {}").format(p)
                    print("q: {}").format(q)
                    try:
                        # Build
                        model = ARMA(dataframe, order=(p,q))
                        model_fit = model.fit()

                        # Evaluate AIC
                        aic = model_fit.aic

                        # store
                        completed[aic] = (p, q)

                        models_tested += 1
                    except Exception as e:
                        print(e)
                        pass

        m = max(completed, key=completed.get)

        # Predict Based on 'Best' Models
        final_model = ARMA(dataframe, order=(completed[m]))
        final_fit = final_model.fit()
        y_hat = final_fit.predict(len(dataframe), len(dataframe) + int(num_pred))

        # Return Preds
        results = y_hat

        # Predict
        return results

    def doSES(self, dataframe, num_pred):

        # dataframe = dataframe.transpose()

        # Grid Search Params
        p_grid = [0,1,2,4,6,8,10]
        q_grid = [0,1,2,3]
        completed = {}

        # models_tested = 0
        # for p in p_grid:
        #     for q in q_grid:
        #             print("p: {}").format(p)
        #             print("q: {}").format(q)
        #             try:
        #                 # Build
        #                 model = ARIMA(dataframe)
        #                 model_fit = model.fit()

        #                 # Evaluate AIC
        #                 aic = model_fit.aic

        #                 # store
        #                 completed[aic] = (p, diff, q)

        #                 models_tested += 1
        #             except:
        #                 pass

        # print(models_tested)
        # print(completed)

        # m = max(completed, key=completed.get)

        # Predict Based on 'Best' Models
        final_model = ExponentialSmoothing(dataframe)
        final_fit = final_model.fit()
        y_hat = final_fit.predict(0, int(num_pred))

        # Return Preds
        results = y_hat

        return results
    
    def export(self, filename):
        return True

    def save(self, data):
        return True
