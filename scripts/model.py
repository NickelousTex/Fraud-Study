import numpy as np
import pandas as pd
import pickle
from scripts.processing import *
from sklearn.ensemble import GradientBoostingClassifier
import requests
import json

class MyModel():

    def __init__(self):
        self.model = GradientBoostingClassifier(learning_rate=0.2,
                                                max_depth=12,
                                                max_features=1.0,
                                                min_samples_leaf=100,
                                                n_estimators=300)

    def fit(self, X, y):
        self.model = self.model.fit(X, y)

        return self

    def predict(self, X):
        prediction = self.model.predict(X)
        return prediction

    def predict_proba(self, X):
        proba = self.model.predict_proba(X)
        return proba

def get_data(datafile):
    data = pd.read_json(datafile)
    data = clean_data(data) #clean data

    y = data['fraud']
    X = data.drop('fraud', axis=1)

    return X, y



if __name__ == '__main__':
    X, y = get_data('data/data.json')
    model = MyModel()
    model.fit(X, y)
    with open('data/model1.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)
