# -*- coding:utf-8 -*-
import json
import config
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

twitter = OAuth1Session(CK, CS, AT, ATS)
# ここまでは全ファイル同じ

url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
params = {'count': 10}
response = twitter.get(url, params=params)

if response.status_code == 200:
    timeline = json.loads(response.text)
    for tweet in timeline:
        print('')
        print(tweet['user']['name'] + ' : ' + tweet['text'])
        print(tweet['created_at'])
        print('----------------------------------------------------')
else:
    print("ERROR: {}".format(response.status_code))

print('\n', '\nt', '\nw', '\ni', '\ncomplete!!!!!!!!!!!', '\nt', '\ne', '\nr', '\n')
