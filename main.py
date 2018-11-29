#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, logging, Response, redirect, flash
import pandas as pd
import os
from agent import TwitterAPI
import config

# 1. make TwitterAPI instance
api = TwitterAPI(
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    access_token=config.ACCESS_TOKEN,
    access_secret=config.ACCESS_SECRET
)

# 2. make Flask instance
app = Flask(__name__)

# 3. item from twitter
columns = [
    'tweet_id',
    'created_at',
    'text',
    'fav',
    'retweets'
]


def get_tweets_df(user_id):
    tweets_df = pd.DataFrame(columns=columns)

    return tweets_df


def get_profile(user_id):
    profile = {}
    return profile


def grouped_df(tweets_df):
    grouped_df = {}
    return grouped_df


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # from the form whose name attribute of the input component is 'user_id'
        user_id = request.form['user_id']
        user_id += 'Pythonista'
        # tweets_df = get_tweets_df(user_id)
        # grouped_df = get_grouped_df(tweets_df)
        # sorted_df = get_sorted_df(tweets_df)
        return render_template(
            'index.html',
            # keyword user_id is coresspond to template {{ user_id }}.
            user_id=user_id

            # tweets_df=tweets_df,
            # grouped_df=grouped_df,
            # sorted_df=sorted_df
        )
    else:
        return render_template('index.html')


# get tweet functions
"""
欲しいのはユーザーの
"""
# 1では、まずget_tweets_df関数で、
# PandasのDataFrame(df)形式でツイートを取得します。その関数はのちほど解説します。

# 2では、取得したDataFrame形式で取得したツイートを、
# 日時集計するget_grouped_df関数で取得します。こちらものちほど解説します。

# 3ではさらに、日時順にツイートを並べるget_sorted_df関数で取得します。

# 4では、ユーザーのプロフィールを取得する関数get_profile関数を呼び出します。
# そして、index.htmlに、取得したそれぞれの値を送信するような処理を行います。


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
