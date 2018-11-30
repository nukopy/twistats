from requests_oauthlib import OAuth1Session
from datetime import datetime
import pandas as pd
import json
import random

import twipy.config as config
import twipy.printdecorator as printdecorator
#import sys; sys.path.append('twipy')


class TwitterAPI:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        print('TwitterAPI instance initialized.\n')
        self.api = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_secret
        )

        # response object
        self.response = None
        self.limit_response = None
        self.resources = None  # limit resources: dic

        # params
        self.search_params = self.set_search_params()
        self.home_timeline_params = self.set_home_timeline_params()
        self.user_timeline_params = self.set_user_timeline_params()
        self.rate_limit_params = self.set_rate_limit_params()

        # paging params
        self.columns = [
            'id',
            'created_at',
            'text',
            'favorite_count',
            'retweet_count'
        ]

    # GET method
    # search
    @printdecorator.print_status_code(http_method='GET', api='search')
    def search_tweets(self) -> object:
        search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        response = self.api.get(search_url, params=self.search_params)
        self.rate_limit_status()  # get request limit
        self.response = response
        return response

    # home_timeline
    @printdecorator.print_status_code(http_method='GET', api='home_timeline')
    def home_timeline(self) -> object:
        home_timeline_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        response = self.api.get(
            home_timeline_url, params=self.home_timeline_params
        )
        self.rate_limit_status()  # get request limit
        self.response = response
        return response

    # user_timeline
    @printdecorator.print_status_code(http_method='GET', api='user_timeline')
    def user_timeline(self) -> object:
        user_timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        response = self.api.get(
            user_timeline_url, params=self.user_timeline_params
        )
        self.rate_limit_status()  # get request limit
        self.response = response
        return response

    # rate_limit_status
    @printdecorator.print_status_code(http_method='GET', api='rate_limit_status')
    def rate_limit_status(self) -> object:
        rate_limit_url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
        limit_response = self.api.get(
            rate_limit_url, params=self.rate_limit_params
        )
        self.limit_response = limit_response
        self.resources = json.loads(limit_response.text)['resources']
        return limit_response

    # set parameter
    # search params

    @printdecorator.print_params(param_name='search')
    def set_search_params(
        self, query='cat cute', count=10, **kwargs
    ) -> dict:
        search_params = {
            'q': query,
            'count': count
        }

        for key, value in kwargs.items():
            search_params[key] = value

        return search_params

    # home_timeline params
    @printdecorator.print_params(param_name='home_timeline')
    def set_home_timeline_params(
        self, count=10, trim_user=True, exclude_replies=True,
        contributor_details=True, include_entities='false', **kwargs
    ) -> dict:
        home_timeline_params = {
            # 'since_id': since_id,
            # 'max_id': max_id,
            'count': count,
            'trim_user': trim_user,
            'exclude_replies': exclude_replies,
            'contributor_details': contributor_details,
            'include_entities': include_entities
        }

        for key, value in kwargs.items():
            home_timeline_params[key] = value

        return home_timeline_params

    # user_timeline params
    @printdecorator.print_params(param_name='user_timeline')
    def set_user_timeline_params(
        self, screen_name='never_be_a_pm', count=200, trim_user=True,
        exclude_replies=True, contributor_details=True, include_rts=True, **kwargs
    ) -> dict:
        """set user_timeline parameters

        Keyword Arguments:
            screen_name {str} -- [description] (default: {'never_be_a_pm'})
            count {int} -- [description] (default: {3200})
            trim_user {bool} -- [description] (default: {True})
            exclude_replies {bool} -- [description] (default: {True})
            contributor_details {bool} -- [description] (default: {True})
            include_rts {bool} -- [description] (default: {True})

        allowed params: allowed_param:'id', 'user_id', 'screen_name', 'since_id', 'max_id', 'count', 'include_rts', 'trim_user', 'exclude_replies'

        Returns:
            dict -- [description]
        """

        user_timeline_params = {
            # 'since_id': since_id,
            # 'max_id': max_id,
            'screen_name': screen_name,
            'count': count,
            'exclude_replies': exclude_replies,
            'trim_user': trim_user,
            'include_rts': True
        }

        for key, value in kwargs.items():
            user_timeline_params[key] = value

        return user_timeline_params

    # rate_limit_status params
    @printdecorator.print_params(param_name='rate_limit_status')
    def set_rate_limit_params(self, resources='user,search,statuses') -> dict:
        rate_limit_params = {'resources': resources}
        return rate_limit_params

    # print GET result
    # print search result
    def print_search_tweets(self) -> None:
        response = self.search_tweets()
        if response.status_code == 200:
            tweets = json.loads(response.text)  # all tweets info
            for tweet in tweets['statuses']:
                print(tweet['user']['name'] + ': ' + tweet['text'])
                print(tweet['created_at'])
                print('-'*20)
        else:
            print('GET failed')
            print('HTTP status code: {}'.format(response.status_code))

    # print home_timeline
    def print_home_timeline(self) -> None:
        response = self.home_timeline()
        if response.status_code == 200:
            home_tweets = json.loads(response.text)
            # tweet = individual tweet(dict-type)
            for tweet in home_tweets:
                print('-'*20)
                print()
                user_id = tweet['user']['name']
                user_tweet = tweet['text']
                time = tweet['created_at']
                print(user_id + ' : ' + user_tweet)
                print(time)
                print('-'*20)
        else:
            print('GET failed')
            print('HTTP status code: {}'.format(response.status_code))

    # print user_timeline
    def print_user_timeline(self) -> None:
        response = self.user_timeline()
        if response.status_code == 200:
            print('request succeed')
            pass
        else:
            print('GET failed')
            print('HTTP status code: {}'.format(response.status_code))

    # print all params
    def print_all_params(self) -> None:
        params = [
            self.search_params.items(),
            self.home_timeline_params.items(),
            self.user_timeline_params.items()
        ]
        for items in params:
            for key, value in items:
                print('{}: {}'.format(key, value))
            print('-'*20)

    # POST method
    # tweet
    def tweet(self, tw_sentence='') -> None:
        # prepare tweet_sentence
        timestamp = datetime.today().strftime('%Y/%m/%d %H:%M')
        if tw_sentence == '':
            messages = ['にゃーん', 'わおーん', 'コケコッコー', '真面目に生きなさい']
            tw_sentence = random.choice(messages)
        tweet_sentence = 'from Python(' + timestamp + ')\n' + tw_sentence

        # request
        tweet_url = 'https://api.twitter.com/1.1/statuses/update.json'
        params = {'status': tweet_sentence}
        response = self.api.post(tweet_url, params=params)
        if response.status_code == 200:  # tweet success
            print('Tweet Succeeded!')
            print('---- tweet_sentence ----')
            print(tweet_sentence, '\n\n')
        else:  # tweet failed
            print('Tweet Failed. : {}'.format(response.status_code))

    # others
    def limit(self):
        limit = res.headers['x-rate-limit-remaining']  # リクエスト可能残数の取得
        reset = res.headers['x-rate-limit-reset']  # リクエスト叶残数リセットまでの時間(UTC)
        # sec = int(res.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple()) #UTCを秒数に変換


if __name__ == '__main__':
    # test
    api = TwitterAPI(
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_secret=config.ACCESS_SECRET
    )

    # api.search_tweets()
    # api.home_timeline()
    res = api.user_timeline()
    # api.tweet(tw_sentence='私は会社に行きたくないです')# api.tweet(tw_sentence='私は会社に行きたくないです')
