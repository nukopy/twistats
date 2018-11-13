#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, logging, Response, redirect, flash
import pandas as pd
import os
from agent import TwitterAPI
import config

# 1. make TwitterAPI instance
api = TwitterAPI(consumer_key=config.CONSUMER_KEY,
                 consumer_secret=config.CONSUMER_SECRET,
                 access_token=config.ACCESS_TOKEN,
                 access_secret=config.ACCESS_SECRET)

# 2. make Flask instance
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return render_template('index.html', user_id=user_id)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
