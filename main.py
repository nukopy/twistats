#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import pandas as pd
from flask import Flask, render_template, request,\
    logging, Response, redirect, flash
from config import CONFIG
import os

# 1. set Twitter key
CONSUMER_KEY = CONFIG['CONSUMER_KEY']
CONSUMER_SECRET = CONFIG['CONSUMER_SECRET']
ACCESS_TOKEN = CONFIG['ACCESS_TOKEN']
ACCESS_SECRET = CONFIG['ACCESS_SECRET']

# 2. get tweepy-api instance
auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY,
                           consumer_secret=CONSUMER_SECRET)
auth.set_access_token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
api = tweepy.API(auth)

# 3. get Flask instance
app = Flask(__name__)

# 4. list


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return render_template('index.html', user_id=user_id)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
