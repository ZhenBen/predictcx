import numpy
import pandas as pd
from pandas.tseries.offsets import BDay
from sklearn.neural_network import MLPClassifier
import pickle

percent_filename = 'percent_change.sav'
change_filename = 'change.sav'

percent_change_model = pickle.load(open(percent_filename, 'rb'))
change_model = pickle.load(open(change_filename, 'rb'))

def predict_percent(data):
    return percent_change_model.predict([data])

def predict_change(data):
    return change_model.predict([data])
