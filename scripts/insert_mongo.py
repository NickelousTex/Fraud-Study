## Takes origional dataframe (prior to column drops) with probability column added and puts in MongoDB database called 'predictions' ##

from pymongo import MongoClient
import json

def add_to_db(test_data):
    '''
    Takes in a pandas row with model prediction
    '''

    # Start Mongo
    client = MongoClient()
    db = client['fraud_db']
    tab = db['predictions']

    #Add to the monogDB
    Add_to_MongoDB = test_data
    Add_to_MongoDB.T.set_index('object_id',inplace=True) #set index to unique ID
    tab.insert_one(json.loads(Add_to_MongoDB.T.to_json()))
