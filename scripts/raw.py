from pymongo import MongoClient
import json
import pandas as pd
import requests

def get_raw():
    #create/verify MongoDB exists
    client = MongoClient()
    db = client['fraud_db']
    tab = db['predictions']

    ##Read and write raw data
    api_key = 'vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC' #API key for reading data
    url = 'https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/'
    sequence_number = 0 #requests
    response = requests.post(url, json={'api_key': api_key,
                                        'sequence_number': sequence_number})
    raw_data = response.json()

    #convert data to PD, then get correct format, then save to JSON
    data = pd.DataFrame.from_dict(raw_data['data'])
    a = pd.DataFrame(data)
    with open('data/raw_data.json', 'w') as fp:
        json.dump(a, fp)

    ##Test to see if data entry already exists:
    print('Checking if entry exists')
    raw = pd.read_json('data/raw_data.json')
    object_check = raw['object_id'][0]
    print('New Entry Beginning...')
    ###Won't work right now- need to check functionality ###
    # return not tab.find({str(object_check):{'$exists':True}}).limit(1).count(True):
