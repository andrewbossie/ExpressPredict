# Title: TimeSeries.py
# Description: Model for saving/retrieving time-series models. (ARIMA, etc)
# Author:
# Date: 

from app import db

class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class TimeSeries(Base):
    __tablename__ = 'series_models'

    def __init__(self, user, data):
        self.user = user
        self.data = data

    def pickleModel(self):
        return 'pickleModel'
    
    def saveModel(self, user, id):
        return 'saved!'

    def retrieveModel(self, user, id):
        return 'model'
