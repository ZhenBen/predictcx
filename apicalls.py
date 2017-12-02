from private import *
import json
import base64
import requests
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions

def twitget(comp, count = 10):
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
    search_params = {
        'q': company[0],
        'result_type': 'mixed',
        'count': count,
        'lang': 'en',
        'tweet_mode':'extended'

    }
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    return search_resp




def watsget(txt):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
      username=watson_username,
      password=watson_password,
      version=watson_version)
    response = natural_language_understanding.analyze(
      text=txt,
      features=Features(
      # Emotion options
      emotion=EmotionOptions([company[0]])
      )
    )
    return response
