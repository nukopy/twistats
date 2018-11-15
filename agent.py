#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
from datetime import datetime
import random
import config


class TwitterAPI:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        print("TwitterAPI instance initialized.")
        self.api = OAuth1Session(client_key=consumer_key,
                                 client_secret=consumer_secret,
                                 resource_owner_key=access_token,
                                 resource_owner_secret=access_secret)
        # search
        self.set_search_params()
        self.current_search_params()

    # search
    def set_search_params(self, query='cat cute', count=10):
        self.search_params = {
            'q': query,
            'count': count
        }

    def current_search_params(self):
        print('current search param')
        for key, value in self.search_params.items():
            print('{}: {}'.format(key, value))
        print('')

    def search_tweets(self):
        # request
        search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        response = self.api.get(search_url, params=this.params)  # response class

        # console output
        if response.status_code == 200:
            tweets = json.loads(response.text)  # all tweets info
            for tweet in tweets["statuses"]:
                print(tweet["user"]["name"] + ': ' + tweet["text"])
                print(tweet["created_at"])
                print("-"*20)
        else:
            print("ERROR!: %d" % response.status_code)

    # timeline
    def set_timelines_params(self, count=10):
        self.timeline_params = {
            'count': count
        }

    def my_timelines(self):
        # request
        timeline_url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        req = self.api.get(timeline_url, params=self.timeline_params)

        # console output
        if req.status_code == 200:
            # count = len(time_line)
            timelines = json.loads(req.text)
            # tweet = individual tweet(dict-type)
            for tweet in timelines:
                print("-"*20)
                print()
                user_id = tweet['user']['name']
                user_tweet = tweet['text']
                time = tweet['created_at']
                print(user_id + ' : ' + user_tweet)
                print(time)
                print('-'*20)
        else:
            print("ERROR: %d" % req.status_code)

    # def limit(self):
    #     limit = res.headers['x-rate-limit-remaining'] #リクエスト可能残数の取得
    #     reset = res.headers['x-rate-limit-reset'] #リクエスト叶残数リセットまでの時間(UTC)
    #     sec = int(res.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple()) #UTCを秒数に変換
    #
    # tweet
    def tweet(self, content=''):
        # prepare tweet_sentence
        timestamp = datetime.today().strftime("%Y/%m/%d %H:%M")
        if content == '':
            messages = ['にゃーん', 'わおーん', 'コケコッコー', '真面目に生きなさい']
            content = random.choice(messages)
        tweet_sentence = 'from Python(' + timestamp + ')\n' + content

        # request
        tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": tweet_sentence}
        response = self.api.post(tweet_url, params=params)
        if response.status_code == 200:  # tweet success
            print('Tweet Succeeded!')
            print('---- tweet_sentence ----')
            print(tweet_sentence, "\n\n")
        else:  # tweet failed
            print("Failed. : {}".format(response.status_code))


if __name__ == '__main__':
    # test
    api = TwitterAPI(consumer_key=config.CONSUMER_KEY,
                     consumer_secret=config.CONSUMER_SECRET,
                     access_token=config.ACCESS_TOKEN,
                     access_secret=config.ACCESS_SECRET)
    # params = api.set_search_params("Deep Learning lang:ja", 20)
    # api.search_tweets(params)
    api.tweet('私は会社に行きたくないです')
