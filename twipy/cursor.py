# Cursor object (for TwiStats)
from configparser import ConfigParser
from datetime import datetime
from bokeh.models import ColumnDataSource, Title, LinearAxis, Range1d, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.tickers import FixedTicker
import pandas as pd
import html.parser
import os
import json

from twipy.api import TwitterAPI


class Cursor(TwitterAPI):
    """ Pagination helper class for TopTweets application"""

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        # super
        super().__init__(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_secret=access_secret
        )

        self.tweets_df = None
        self.profile = None
        # for get_tweets_df's DataFrame columns
        self.columns = [
            'id',
            'created_at',
            'text',
            'favorite_count',
            'retweet_count'
        ]
        # for get_profile
        self.profile_keys = [
            'id',
            'name',
            'screen_name',
            'description',
            'profile_image_url',
            'friends_count',
            'followers_count'
        ]

    def get_tweets_df(self, screen_name='never_be_a_pm', num_tweets=1000):
        """allowed_param: 'id', 'user_id', 'screen_name', 'since_id', 'max_id', 'count', 'include_rts', 'trim_user', 'exclude_replies'"""
        # constant
        tweets_df = pd.DataFrame(columns=self.columns)
        resources_key = '/statuses/user_timeline'
        loop = int(num_tweets / 200)  # 200 = tweets numbers per request

        self.set_user_timeline_params(screen_name=screen_name)
        for _ in range(loop):
            # request
            tweets = self.user_timeline()

            # get limit rate
            limit = self.resources['statuses'][resources_key]
            remaining = limit['remaining']
            reset_time = datetime.fromtimestamp(limit['reset'])
            if self.response.status_code == 200 and tweets:  # tweets != []
                for tweet in tweets:
                    if not 'RT @' in tweet['text']:
                        se = pd.Series([
                            tweet['id'],
                            tweet['created_at'],
                            html.parser.HTMLParser().unescape(
                                tweet['text'].replace('\n', ' ')),
                            tweet['favorite_count'],
                            tweet['retweet_count'],
                        ],
                            index=self.columns,
                        )
                        tweets_df = tweets_df.append(se, ignore_index=True)
                    else:
                        continue

                # pagination: last tweet-id - 1 is next max_id;
                max_id = tweets[-1]['id'] - 1
                self.user_timeline_params['max_id'] = max_id

            else:
                print('GET failed')
                print('HTTP status code: {}\n'.format(
                    self.response.status_code))

            # check API rate limit
            if remaining == 50:
                print(
                    'Max limit rate over.\n'
                    'If you wanna continue to use Twitter API, \n'
                    'please wait until {}'.format(reset_time)
                )
                break

        # cast
        tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'])
        tweets_df['id'] = tweets_df['id'].astype(int)
        tweets_df['favorite_count'] = tweets_df['favorite_count'].astype(int)
        tweets_df['retweet_count'] = tweets_df['retweet_count'].astype(int)

        self.tweets_df = tweets_df
        return tweets_df

    def get_day_grouped_df(self):
        """
        Grouped self.tweets_def by individual days
        *** MUST DO get_tweets def(update self.tweets_df) ***
        """
        day_grouped = self.tweets_df.groupby(
            self.tweets_df.created_at.dt.date
        )  # CAUTION: also occur tweet-'id' summation

        day_grouped_df = day_grouped.sum()
        day_grouped_df['tweets_per_day'] = day_grouped.size()
        self.day_grouped_df = day_grouped_df
        return day_grouped_df

    def get_fav_rt_sorted_df(self, sort_by='retweet_count'):
        # sort_by = 'retweet_count' or 'favorite_count'
        sorted_df = self.tweets_df.sort_values(
            by=sort_by, ascending=False
        )
        self.sorted_df = sorted_df
        return sorted_df

    def get_profile(self, screen_name='never_be_a_pm'):
        # request & update self.response
        user = self.users_show(screen_name=screen_name)

        # make profile-dict
        profile = {
            'id': user['id'],
            'name': user['name'],
            'user_id': user['screen_name'],  # = screen_name
            'description': user['description'],
            'image': user['profile_image_url'],
            'friends_count': user['friends_count'],
            'followers_count': user['followers_count']
        }

        try:
            profile['expanded_url'] = user['entities']['url']['urls'][0]['expanded_url']
        except KeyError as e:
            print('LOG: KeyError: {}'.format(e.args[0]))
            print('"expanded_url" was not added to profile.\n')

        self.profile = profile  # pdb.set_trace()
        return profile

    def plot(self):
        # data
        df = self.day_grouped_df
        source = ColumnDataSource({
            'date': df.index,
            'favorite': df.favorite_count,
            'retweet': df.retweet_count,
            'tweets': df.tweets_per_day
        })

        # select the tools we want
        TOOLS = ['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save']  # 'hover'
        TOOLTIPS = """
        
            <div style="font-weight: bold;">@date{%y/%m/%d}</div>
            <div>
                <span style="color: #e0245e; font-weight: bold;"><i class="fas fa-heart"></i> <span class="pull-right">@favorite{0}<span></span>
            </div>
            <div>
                <span style="color: #17bf63; font-weight: bold;"><i class="fas fa-retweet"></i> <span class="pull-right">@retweet{0}<span></span>
            </div>
            <div>
                <span style="color: #1da1f2; font-weight: bold;"><i class="fab fa-twitter"></i> <span class="pull-right">@tweets{0}<span></span>
            </div>
        """

        # prepare fig
        fig = figure(
            plot_width=800, plot_height=600, sizing_mode='scale_width',
            x_axis_type='datetime', tools=TOOLS
        )
        hover = HoverTool(
            tooltips=TOOLTIPS,
            formatters={'date': 'datetime'}
        )
        fig.add_tools(hover)

        # title
        background_color = '#e6ecf0'  # #c0cad1'
        fig.add_layout(Title(
            text='{} ~ {}'.format(df.index.min(), df.index.max()),
            text_font_size='16px', align='center'), 'above')
        fig.add_layout(Title(
            text='Fav & RT & Tweets / day',
            text_font_size='18px', align='center'), 'above')
        fig.title.text_font_style = 'bold'
        fig.title.text_font_size = '20px'

        # Axis
        fig.xaxis.axis_label = 'Date'
        fig.yaxis.axis_label = 'Favorite & Retweet'
        fig.xaxis.major_label_orientation = 0.8
        # second axis
        # Setting the second y axis range name and range
        fig.extra_y_ranges = {"tweets": Range1d(
            start=-1, end=df.tweets_per_day.max()+3)}
        # Adding the second axis to the plot.
        fig.add_layout(
            LinearAxis(y_range_name="tweets", axis_label='Tweets'),
            'right'
        )
        fig.xaxis.axis_label_text_font_size = '17px'
        fig.xaxis.major_label_text_font_size = '15px'
        fig.yaxis.axis_label_text_font_size = '17px'
        fig.yaxis.major_label_text_font_size = '15px'

        # Grid
        fig.xgrid.grid_line_color = '#98a0a5'
        fig.xgrid.grid_line_alpha = 0.3
        fig.ygrid.grid_line_color = '#98a0a5'
        fig.ygrid.grid_line_alpha = 0.3

        # plot
        line_alpha = 0.6
        # favorite
        fig.line(
            x='date', y='favorite', source=source,
            line_color=(255, 99, 132, line_alpha), line_width=3
        )
        fig.circle(
            x='date', y='favorite', source=source, size=5,
            fill_color=(255, 99, 132, 0.3),
            line_color=(255, 99, 132, line_alpha), line_width=3,
            legend='Favorite'
        )

        # retweet
        fig.line(
            x='date', y='retweet', source=source,
            line_color='#17bf63', line_width=3, line_alpha=line_alpha
        )
        fig.circle(
            x='date', y='retweet', source=source, size=5,
            fill_color='#17bf63', fill_alpha=0.3,
            line_color='#17bf63', line_alpha=line_alpha, line_width=3,
            legend='Retweet'
        )

        # tweet
        tw_alpha = 0.3
        fig.line(
            x='date', y='tweets', source=source,
            line_color='#428bca', line_width=4, line_alpha=tw_alpha,
            y_range_name='tweets'
        )
        fig.circle(
            x='date', y='tweets', source=source, size=4,
            line_alpha=0, fill_color='#428bca', fill_alpha=tw_alpha,
            y_range_name='tweets',
            legend='Tweets'
        )

        # fig.xaxis.ticker = FixedTicker(ticker=self.tweets_df.created_at)
        fig.background_fill_color = background_color
        fig.border_fill_color = background_color
        fig.toolbar.autohide = True

        # legend config
        lgd_alpha = 0.8
        fig.legend.location = 'top_left'
        # legend: background
        fig.legend.background_fill_color = background_color
        fig.legend.background_fill_alpha = lgd_alpha
        fig.legend.label_text_font_size = '10pt'
        fig.legend.label_text_font_style = 'bold'
        # fig.legend.click_policy = 'mute'

        # for embed  in webpages
        # import pdb
        # pdb.set_trace()
        script, div = components(
            models=fig, wrap_script=True, wrap_plot_info=True
        )

        return script, div


if __name__ == "__main__":
    api = Cursor(
        consumer_key=os.environ['TW_CONSUMER_KEY'],
        consumer_secret=os.environ['TW_CONSUMER_SECRET'],
        access_token=os.environ['TW_ACCESS_TOKEN'],
        access_secret=os.environ['TW_ACCESS_SECRET'],
    )

    df = api.get_tweets_df(screen_name='mathnuko')
    user = api.get_profile()
    day_grouped_df = api.get_day_grouped_df()
    # fav_rt_sorted_df = api.get_fav_rt_sorted_df()
