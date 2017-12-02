
#DocumentEmotionResult
from private import *
import json
import base64
import requests
import numpy
import pandas as pd
from pandas.tseries.offsets import BDay
from sklearn.neural_network import MLPClassifier
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
import pickle

companies = [["Microsoft", "MSFT"], ["Apple","AAPL"],["Google", "GOOGL"],
            ["Amazon","AMZN"], ["IBM","IBM"],["SAP","SAP"],["Oracle","ORCL"],
            ["Netflix","NFLX"],["Tesla","TSLA"],["Disney","DIS"]]

#AUTHORIZATION
key_secret = '{}:{}'.format(twitter_consumer_key, twitter_consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = twitter_url
auth_url = '{}oauth2/token'.format(base_url)
search_url = '{}1.1/search/tweets.json'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {'grant_type': 'client_credentials'}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = auth_resp.json()['access_token']
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

#IBM INFO
natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=watson_username,
  password=watson_password,
  version=watson_version)


company_scores={}
for company in companies:
    print('calculating emotions for ' + company[0])
    company_scores[company[0]]={
        'sadness': 0,
        'disgust': 0,
        'anger': 0,
        'joy': 0,
        'fear': 0
    }
    score=[]
    count = 2
    search_params = {
        'q': company[0],
        'result_type': 'mixed',
        'count': count,
        'lang': 'en',
        'tweet_mode':'extended'

    }
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    for tweet in search_resp.json()['statuses']:
        response = natural_language_understanding.analyze(
          text=tweet['full_text'],
          features=Features(
          # Emotion options
          emotion=EmotionOptions([company[0]])
          )
        )
        score.append(response['emotion']['document']['emotion'])

    for s in score:
        company_scores[company[0]]['sadness'] += (s['sadness'] / count)
        company_scores[company[0]]['disgust'] += (s['disgust'] / count)
        company_scores[company[0]]['anger'] += (s['anger'] / count)
        company_scores[company[0]]['joy'] += (s['joy'] / count)
        company_scores[company[0]]['fear'] += (s['fear'] / count)

print(company_scores)

# STOCKCHANGES
stock_changes = {}
for company in companies:
    print('calculating stock for ' + company[0])
    stock_params = {
        'function':'TIME_SERIES_DAILY',
        'symbol': company[1],
        'apikey': stock_api_key
    }
    response = requests.get(stock_url, params=stock_params)
    today = pd.datetime.today()
    if ((today - BDay(0)) == today):
        last_business = today
    else:
        last_business = today - BDay(1)
    week_ago = last_business - BDay(7)
    last_business_stock = response.json()["Time Series (Daily)"][last_business.strftime('%Y-%m-%d')]
    week_ago_stock = response.json()["Time Series (Daily)"][week_ago.strftime('%Y-%m-%d')]
    change = (float(last_business_stock['4. close']) - float(week_ago_stock['4. close']))/float(week_ago_stock['4. close'])
    stock_changes[company[0]] = change

print(stock_changes)

print('Constructing Neural Network real data scientists!!!!')
mlp = MLPClassifier(hidden_layer_sizes=(10,10,10))
X = []
y = []
for company in companies:
    data = []
    data.append(company_scores[company[0]]['sadness'])
    data.append(company_scores[company[0]]['disgust'])
    data.append(company_scores[company[0]]['anger'])
    data.append(company_scores[company[0]]['joy'])
    data.append(company_scores[company[0]]['fear'])
    X.append(data)
    y.append(int(stock_changes[company[0]]*10000))

print(X)
print(y)
mlp.fit(X,y)

model_file = 'percent_change.sav'
pickle.dump(mlp, open(model_file, 'wb'))

y2=[]
for i in y:
    if i < 0:
        y2.append('negative')
    else:
        y2.append('positive')

mlp2 = MLPClassifier(hidden_layer_sizes=(10,10,10))
mlp2.fit(X,y2)

model_file = 'change.sav'
pickle.dump(mlp2, open(model_file, 'wb'))
