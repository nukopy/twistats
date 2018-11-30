import pandas as pd
import json
from datetime import datetime
from twipy.api import TwitterAPI
import config


class Cursor(TwitterAPI):
    """ Pagination helper class"""

    def paging(self, screen_name='never_be_a_pm', num_tweets=1000):
        # container DataFrame for output
        tweet_df = pd.DataFrame(columns=self.columns)
        resources_key = '/statuses/user_timeline'
        loop = int(num_tweets / 200)  # 200 = tweets numbers per request

        self.set_user_timeline_params(screen_name=screen_name)
        for _ in range(loop):
            # request
            self.user_timeline()  # update self.response
            self.rate_limit_status()  # update self.limit_response, self.sources
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

        return tweet_df


if __name__ == "__main__":
    api = Cursor(
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_secret=config.ACCESS_SECRET
    )
    df = api.paging()
