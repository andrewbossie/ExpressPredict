from app import db
import matplotlib as plt
import numpy as np
import pandas as pd 
import statsmodels
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.tools import diff
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

        # Parse file
        if ext.lower() == "csv":
            df = pd.read_csv(filename)
        else:
            df = pd.read_excel(filename)

        # Flatten / sum row data
        df_flat = pd.DataFrame(df.sum(axis=0))
        df_flat = df_flat.to_numpy()

        return df_flat

    # Scale Data
    def doStandardScale(self, dataframe):
        scaler = StandardScaler()
        scaled = scaler.fit_transform(dataframe)
        return scaled
        
    # Regularize
    def doNormalize(self, dataframe):
        minScaler = MinMaxScaler()
        minMax = minScaler.fit_transform(dataframe)
        return minMax

     # Make Stationary
    def doStationary(self, dataframe):
        stationary = diff(dataframe)
        return stationary

    # Inverse Preprocessing Methods
    def doStandardScaleRevert(self, dataframe):
        scaler = StandardScaler()
        scaled = scaler.inverse_transform(dataframe)
        return scaled
        
    def doNormalizeRevert(self, dataframe):
        minScaler = MinMaxScaler()
        minMax = minScaler.inverse_transform(dataframe)
        return minMax

    def doStationaryRevert(self, original_df, formatted_df):
        return True

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

    def predict(self, model, amount):
        return True
    
    def export(self, filename):
        return True

    def save(self, data):
        return True
