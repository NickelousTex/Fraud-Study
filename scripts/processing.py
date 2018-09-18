import pandas as pd

def clean_data(df):

    #needed to verify & create currency match column
    Country_dictionary= {'IE': 'EUR', 'FR': 'EUR', 'ES': 'EUR', 'NL': 'EUR', 'DE': 'EUR', 'BE': 'EUR', 'AT': 'EUR', 'PT': 'EUR', 'IT': 'EUR', 'HU': 'EUR', 'RO': 'EUR', 'CZ': 'EUR', 'FI': 'EUR', 'HR': 'EUR', 'BG': 'EUR', 'SI': 'EUR', 'SE': 'EUR', 'DK': 'EUR', 'US': 'USD', 'CA': 'CAD', 'GB': 'GBP', 'AU': 'AUD', 'NZ': 'NZD', 'MX': 'MXN'}
    #needed for drop all unneeded columns
    DROP = ['approx_payout_date', 'body_length',
            'description','email_domain',
           'event_created', 'event_end', 'event_published', 'event_start',
           'has_header',
           'listed', 'name', 'name_length', 'num_payouts',
           'object_id', 'org_desc', 'org_facebook', 'org_name', 'org_twitter',
           'payee_name', 'sale_duration',
           'sale_duration2',  'ticket_types',
           'user_created', 'user_type', 'venue_address', 'venue_country',
           'venue_latitude', 'venue_longitude', 'venue_name', 'venue_state','payout_type','previous_payouts',
           'country','currency', 'length_before_event', 'event_published', 'acct_type']

    fraud = ['fraudster_event','spammer_warn', 'fraudster',
           'spammer_limited', 'spammer_noinvite', 'locked', 'tos_lock',
           'tos_warn', 'fraudster_att', 'spammer_web', 'spammer']

    df['fraud'] = False
    df['fraud'].loc[df['acct_type'] != 'premium'] = True

    #Needed new Columns
    ## Clean Code
    df['event_length'] = df['event_end'] - df['event_start']
    df['length_before_event'] = df['event_published'] - df['event_created']
    df['event_published_present'] = df['event_published']
    df['event_published_present'] = df['event_published_present'].isnull()
    df['event_published_present'].replace(to_replace=[False, True], value=[2,3], inplace=True)
    df['event_published_present'].replace(to_replace=[2,3], value=[1,0], inplace=True)

    df['payout_type'].loc[df['payout_type'] == 'ACH'] = 'ACH'
    df['payout_type'].loc[df['payout_type'] == 'CHECK'] = 'CHECK'
    df['payout_type'].loc[df['payout_type'] == ''] = 'No payout_type listed'
    #new previous payouts
    df['num_previous_payouts'] = list(map(len, df['previous_payouts']))

    #inplace methods
    df['country'].replace('', None,inplace = True)
    df['delivery_method'].fillna(value=4,inplace=True)
    df['currency_match']=(df['country'].map(Country_dictionary) == df['currency']).replace([True,False],[1,0])
    df['venue_name_exits'] = df['venue_name'].isnull().replace([False, True], [0,1])

    #hard code dummies for email_domain
    df['email_gmail'] = 0
    df['email_gmail'].loc[df['email_domain'].str.contains('gmail')] = 1
    df['email_yahoo'] = 0
    df['email_yahoo'].loc[df['email_domain'].str.contains('yahoo')] = 1
    df['email_aol'] = 0
    df['email_aol'].loc[df['email_domain'].str.contains('aol')] = 1
    df['email_hotmail'] = 0
    df['email_hotmail'].loc[df['email_domain'].str.contains('hotmail')] = 1
    # user age listed dummy variable
    df['user_age_listed'] = True
    df['user_age_listed'].loc[df['user_age'] == 0] = False

    #get dummies
    country_dummies = pd.get_dummies(df['country'])
    currency_dummies = pd.get_dummies(df['currency'])
    delivery_dummy = pd.get_dummies(df['delivery_method'])
    payout_type = pd.get_dummies(df['payout_type'])

    #dummy variables to concate at end
    dummy_add = [df, country_dummies, currency_dummies, delivery_dummy, payout_type]

    #Drop Everything We Don't Need -- CAREFUL
    df.drop(DROP,axis = 1,inplace=True)

    #add it all together
    final_df = pd.concat(dummy_add, axis=1)

    return final_df

def clean_test_data(datafile):
    # script to process and clean inputted test data
    df_test = pd.read_json(datafile)
    df_orig = pd.read_csv('data/data_cleaned.csv') # must read in dummy

    df_merge = pd.concat((df_test, df_orig))
    df_merge_clean = clean_data(df_merge)

    df_test_new = df_merge_clean.iloc[0, :] # return cleaned test data

    # y = df_test_new['fraud']
    X = df_test_new.drop('fraud')
    X.fillna(0, inplace=True)
    return X
