#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import config


class TwitterAPI:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        print("TwitterAPI instance initialized.")
        self.api = OAuth1Session(client_key=consumer_key,
                                 client_secret=consumer_secret,
                                 resource_owner_key=access_token,
                                 resource_owner_secret=access_secret)

    def make_search_params(self, query="cat cute", count=20):
        params = {
            'q': query,
            'count': count
        }
        return params

    def search_tweet(self, params):
        # request
        search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        response = self.api.get(search_url, params=params)  # response class

        # console output
        if response.status_code == 200:
            tweets = json.loads(response.text)  # all tweets info
            for tweet in tweets["statuses"]:
                print(tweet["user"]["name"] + ': ' + tweet["text"])
                print(tweet["created_at"])
                print("-"*20)
        else:
            print("ERROR!: %d" % response.status_code)

    def get_timeline(self, params={"count": 10}):
        # request
        timeline_url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        req = self.api.get(timeline_url, params=params)

        # console output
        if req.status_code == 200:
            # count = len(time_line)
            time_line = json.loads(req.text)
            """
            variable: tweet(dict)
            key: following
                created_at: time
                id, id_str
                text : tweets-sentence
                truncated
                entities
                source
                in_reply_to_status_id
                in_reply_to_status_id_str
                in_reply_to_user_id
                in_reply_to_user_id_str
                in_reply_to_screen_name
                *** user: all-tweet infomation
                geo
                coordinates
                place
                contributors
                retweeted_status
                is_quote_status
                retweet_count
                favorite_count
                favorited
                retweeted
                lang
            """
            # tweet = individual tweet(dict-type)
            for tweet in time_line:
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


if __name__ == '__main__':
    api = TwitterAPI(consumer_key=config.CONSUMER_KEY,
                     consumer_secret=config.CONSUMER_SECRET,
                     access_token=config.ACCESS_TOKEN,
                     access_secret=config.ACCESS_SECRET)
    params = api.make_search_params("Deep Learning lang:ja", 20)
    api.search_tweet(params)
