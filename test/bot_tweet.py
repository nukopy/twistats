#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import datetime
from agent import TwitterAPI
import config


def main():
    api = TwitterAPI(consumer_key=config.CONSUMER_KEY,
                     consumer_secret=config.CONSUMER_SECRET,
                     access_token=config.ACCESS_TOKEN,
                     access_secret=config.ACCESS_SECRET)

    # prepare tweet_sentence
    timestamp = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")
    messages = ['にゃーん', 'わおーん', 'コケコッコー', '真面目に生きなさい']
    tweet = random.choice(messages)
    tweet_sentence = 'from Python(' + timestamp + ')\n' + tweet

    # request
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {"status": tweet_sentence}
    response = api.api.post(tweet_url, params=params)

    if response.status_code == 200:  # tweet success
        print('Tweet Succeeded!')
        print('---- tweet_sentence ----')
        print(tweet_sentence, "\n\n")
    else:  # tweet failed
        print("Failed. : {}".format(response.status_code))


if __name__ == '__main__':
    main()
