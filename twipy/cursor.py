# Cursor object (for TopTweets)
import pandas as pd
import json
from datetime import datetime
from twipy.api import TwitterAPI
import config


class TopTweets(TwitterAPI):
    """ Pagination helper class for TopTweets application"""

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        # super
        super().__init__(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_secret=access_secret
        )

        # attributes
        self.tweets_df = None
        self.profile = None

    def get_tweets_df(self, screen_name='never_be_a_pm', num_tweets=1000):
        # container DataFrame for output
        tweet_df = pd.DataFrame(columns=self.columns)
        resources_key = '/statuses/user_timeline'
        loop = int(num_tweets / 200)  # 200 = tweets numbers per request

        self.set_user_timeline_params(screen_name=screen_name)
        for _ in range(loop):
            # request
            self.user_timeline()  # update self.response
            tweets = json.loads(self.response.text)

            # limit rate
            limit = self.resources['statuses'][resources_key]
            remaining = limit['remaining']
            reset_time = datetime.fromtimestamp(limit['reset'])

            # store tweet to df
            for tweet in tweets:
                if not 'RT @' in tweet['text']:
                    # tweet.keys()
                    se = pd.Series([
                        tweet['id'],
                        tweet['created_at'],
                        tweet['text'].replace('\n', ''),
                        tweet['favorite_count'],
                        tweet['retweet_count'],
                    ],
                        index=self.columns,
                    )
                    tweet_df = tweet_df.append(se, ignore_index=True)
                else:
                    continue

            # pagination
            max_id = tweet['id'] - 1  # last tweet-id is next max_id
            self.user_timeline_params['max_id'] = max_id

            # check API rate limit
            if remaining == 0:
                print(
                    'Max limit rate over.\n'
                    'If you wanna continue to use Twitter API, \n'
                    'please wait until {}'.format(reset_time)
                )
                break

        # cast to datetime
        tweet_df['created_at'] = pd.to_datetime(tweet_df['created_at'])
        self.tweets_df = tweet_df
        return tweet_df

    def get_profile(self, screen_name='never_be_a_pm'):
        self.users_show(screen_name=screen_name)  # update self.response
        user = json.loads(self.response.text)
        profile = {
            'id': user['id'],
            'name': user['name'],
            'user_id': user['screen_name'],  # = screen_name
            'description': user['description'],
            'expanded_url': user['entities']['url']['urls'][0]['expanded_url'],
            'image': user['profile_image_url'],
            'friends_count': user['friends_count'],
            'followers_count': user['followers_count']
        }
        self.profile = profile
        return profile

    def get_day_grouped_df(self):
        day_grouped_df = self.tweets_df.groupby(
            self.tweets_df.created_at.dt.date
        ).sum()  # also occur 'id' summation
        return day_grouped_df

    def get_fav_rt_sorted_df(self, sort_by='retweet_count'):
        # sort_by = 'retweet_count' or 'favorite_count'
        sorted_df = self.tweets_df.sort_values(
            by=sort_by, ascending=False
        )
        return sorted_df


if __name__ == "__main__":
    api = TopTweets(
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_secret=config.ACCESS_SECRET
    )
    df = api.get_tweets_df()
    user = api.get_profile()
    day_grouped_df = api.get_day_grouped_df()
    fav_rt_sorted_df = api.get_fav_rt_sorted_df()
