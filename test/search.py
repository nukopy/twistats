#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import config


twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/search/tweets.json"

print('')
print("What do you search?")
keyword = input('>> ')
print('----------------------------------------------------')

params = {'q': keyword, 'count': 10}
req = twitter.get(url, params=params)

if req.status_code == 200:
    search_time_line = json.loads(req.text)
    for tweet in search_time_line['statuses']:
        print(tweet['user']['name'] + '::' + tweet['text'])
        print(tweet['created_at'])
        print('----------------------------------------------------')
else:
    print("ERROR: %d" % req.status_code)
