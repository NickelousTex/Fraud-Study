from scripts.model import *
from scripts.processing import *
import pickle
import pandas as pd
from scripts.insert_mongo import *
import json
import requests
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

def predict():

    print('Loading model...')
    # model = pickle.load(open('data/model1.pkl', 'rb'))

    #Trying this instead of the above line
    with open('data/model1.pkl', 'rb') as f:
        model = pickle.load(f)


    print('Cleaning test data...')
    X_test = clean_test_data('data/raw_data.json')
    print('Making prediction...')
    prediction = model.predict(X_test.values.reshape(1, -1))
    print("Predicted fraud?: {}".format(prediction[0]))

    proba = model.predict_proba(X_test.values.reshape(1, -1))
    print("Probability of Fraud: {:.3f}".format(proba[0][1]))

    # Create output file to push to db
    jj = json.load(open('data/raw_data.json'))
    
    df = pd.read_json(jj)
    output = df.iloc[0,:]
    output['prediction'] = prediction

    # Export to json file
    print('Exporting to database...')
    output = output.to_frame()
    add_to_db(output)

    print('Finished.')

    return prediction, proba


if __name__ == '__main__':
    
    sched = BlockingScheduler()
    sched.add_job(predict,'interval',seconds=2)
    # frame = pd.read_json('data/raw_data.json')
    # sched.add_job((lambda: add_to_db(frame))
    sched.start()
