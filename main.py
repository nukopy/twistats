# TopTweets
from flask import Flask, render_template, request, send_file
from configparser import ConfigParser
import pandas as pd
import datetime

from twipy.api import TwitterAPI
from twipy.cursor import TopTweets
import twipy.config as config


# get config
config = ConfigParser()
config.read('config.ini')
section = 'OAuth'
CK = config.get(section, 'CONSUMER_KEY')
CS = config.get(section, 'CONSUMER_SECRET')
AT = config.get(section, 'ACCESS_TOKEN')
AS = config.get(section, 'ACCESS_SECRET')

#  generate Flask instance & TwitterAPI instance
app = Flask(__name__)
api = TopTweets(
    consumer_key=CK,
    consumer_secret=CS,
    access_token=AT,
    access_secret=AS
)

# config jinja2 filter


def dt_filter(dt: datetime.datetime):
    return dt.strftime('%I:%M %p - %a, %b %d, %Y')


app.jinja_env.filters['dt_filter'] = dt_filter


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        if user_id != '' and not (2 <= len(user_id.split(' '))):
            tweets_df = api.get_tweets_df(screen_name=user_id)
            # judge protected FIXME
            if api.response.status_code == 200 and len(tweets_df.index) != 0:
                profile = api.get_profile(screen_name=user_id)
                day_grouped_df = api.get_day_grouped_df()
                sorted_df = api.get_fav_rt_sorted_df(sort_by='favorite_count')
                script, div = api.plot()

                # summary
                dt = day_grouped_df.index  # datetime index
                days = (dt.max() - dt.min()).days  # timedelta to int
                list_weekday = ['Monday', 'Tuesday', 'Wednesday',
                                'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday = pd.value_counts(tweets_df.created_at.dt.weekday)
                hour = pd.value_counts(tweets_df.created_at.dt.hour)
                ave_tweets = tweets_df.shape[0] / days if days != 0 else 0
                summary = {
                    'max_fav': tweets_df.favorite_count.max(),
                    'max_rt': tweets_df.retweet_count.max(),
                    'ave_tweets': ave_tweets,
                    'max_tweets': day_grouped_df.tweets_per_day.max(),
                    'weekday': list_weekday[weekday.idxmax()],
                    'period': f'{hour.idxmax()}:00 ~ {hour.idxmax() + 1}:00'
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
    df = df.drop(['id', 'text'], axis=1)
    df.to_csv('outputs/day_grouped.csv', encoding='utf-8')
    return send_file(
        'outputs/day_grouped.csv',
        mimetype='text/csv',
        attachment_filename='day_grouped.csv',
        as_attachment=True
    )


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
