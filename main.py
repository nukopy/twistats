# TopTweets
from flask import Flask, render_template, request, logging, Response, redirect, flash
import pandas as pd
import os

from twipy.api import TwitterAPI
from twipy.cursor import TopTweets
import twipy.config as config


#  generate Flask instance & TwitterAPI instance
app = Flask(__name__)
api = TopTweets(
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    access_token=config.ACCESS_TOKEN,
    access_secret=config.ACCESS_SECRET
)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # name' attribute of the input component is 'user_id'
        user_id = request.form['user_id']
        user_id += 'Pythonista'

        return render_template(
            'index.html',
            profile=api.get_profile(screen_name=user_id),
            user_id=user_id,
            tweets_df=api.get_tweets_df(),
            day_grouped_df=api.get_day_grouped_df(),
            sorted_df=api.get_fav_rt_sorted_df(sort_by='retweet_count')
        )
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
