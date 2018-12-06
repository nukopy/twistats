# TopTweets
from flask import Flask, render_template, request, send_file
from configparser import ConfigParser
import pandas as pd
import datetime
import re
import os

from twipy.api import TwitterAPI
from twipy.cursor import Cursor


#  generate Flask instance & TwitterAPI instance
app = Flask(__name__)
api = Cursor(
    consumer_key=os.environ['TW_CONSUMER_KEY'],
    consumer_secret=os.environ['TW_CONSUMER_SECRET'],
    access_token=os.environ['TW_ACCESS_TOKEN'],
    access_secret=os.environ['TW_ACCESS_SECRET'],
)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        if user_id != '' and not (2 <= len(user_id.split(' '))):
            tweets_df = api.get_tweets_df(
                screen_name=user_id)  # update self.tweets_df
            # judge protected FIXME
            if api.response.status_code == 200 and len(tweets_df.index) != 0:
                tweets_df['numbers_of_characters'] = tweets_df['text'].map(
                    text_length).astype(int)
                api.tweets_df = tweets_df
                profile = api.get_profile(screen_name=user_id)
                day_grouped_df = api.get_day_grouped_df()
                sorted_df = api.get_fav_rt_sorted_df(sort_by='favorite_count')
                script, div = api.plot()

                # summary
                dt = day_grouped_df.index  # datetime index
                num_tweets = tweets_df.shape[0]
                days = (dt.max() - dt.min()).days  # timedelta to int
                list_weekday = ['Monday', 'Tuesday', 'Wednesday',
                                'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday = pd.value_counts(tweets_df.created_at.dt.weekday)
                hour = pd.value_counts(tweets_df.created_at.dt.hour)
                ave_tweets = num_tweets / days if days != 0 else 0
                length = tweets_df['numbers_of_characters'].sum(
                ) / num_tweets if num_tweets != 0 else 0
                summary = {
                    'max_fav': tweets_df.favorite_count.max(),
                    'max_rt': tweets_df.retweet_count.max(),
                    'ave_tweets': ave_tweets,
                    'max_tweets': day_grouped_df.tweets_per_day.max(),
                    'weekday': list_weekday[weekday.idxmax()],
                    'period': f'{hour.idxmax()}:00 ~ {hour.idxmax() + 1}:00',
                    'length': length
                }

                return render_template(
                    'index.html',
                    script=script,
                    div=div,
                    profile=profile,
                    user_id=user_id,
                    tweets_df=tweets_df,
                    day_grouped_df=day_grouped_df,
                    sorted_df=sorted_df,
                    summary=summary
                )
            else:
                return render_template(
                    'index.html',
                    user_id=user_id,
                    not_found="was not found"
                )
        elif not user_id:
            return render_template(
                'index.html',
                user_id=user_id,
                error_msg="Please enter IDs."
            )
        elif 2 <= len(user_id.split(' ')):
            return render_template(
                'index.html',
                user_id=user_id,
                error_msg="Please enter IDs NOT separated by space."
            )
    else:
        return render_template('index.html')


@app.route('/tweets_csv', methods=['GET'])
def tweets_csv():
    df = api.tweets_df
    df = df.drop(['id'], axis=1)
    df.to_csv('outputs/tweets.csv', encoding='utf-8')
    return send_file(
        'outputs/tweets.csv',
        mimetype='text/csv',
        attachment_filename='tweets.csv',
        as_attachment=True
    )


@app.route('/day_grouped_csv', methods=['GET'])
def day_grouped_csv():
    df = api.day_grouped_df
    df = df.drop(['id'], axis=1)
    df.to_csv('outputs/day_grouped.csv', encoding='utf-8')
    return send_file(
        'outputs/day_grouped.csv',
        mimetype='text/csv',
        attachment_filename='day_grouped.csv',
        as_attachment=True
    )


def text_length(text: str):
    # numbers of characters
    sub = re.sub(pattern, '', text)
    sub = re.sub('\s', '', sub)
    return len(sub)


def dt_filter(dt: datetime.datetime):
    # filter for jinja2
    return dt.strftime('%I:%M %p - %a, %b %d, %Y')


# helper func
app.jinja_env.filters['dt_filter'] = dt_filter
# pattern = re.compile('https?://.+\s?')
pattern = re.compile('https?://[\w./]+\s?')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
