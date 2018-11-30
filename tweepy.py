# __init__.py
"""
Tweepy Twitter API library
"""
__version__ = '3.7.0'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from tweepy.models import Status, User, DirectMessage, Friendship, SavedSearch, SearchResults, ModelFactory, Category
from tweepy.error import TweepError, RateLimitError
from tweepy.api import API
from tweepy.cache import Cache, MemoryCache, FileCache
from tweepy.auth import OAuthHandler, AppAuthHandler
from tweepy.streaming import Stream, StreamListener
from tweepy.cursor import Cursor

# Global, unauthenticated instance of API
api = API()


def debug(enable=True, level=1):
    from six.moves.http_client import HTTPConnection
    HTTPConnection.debuglevel = level


# get_tweets_df
@property
def user_timeline(self):
    """ :reference: https://dev.twitter.com/rest/reference/get/statuses/user_timeline
        :allowed_param:'id', 'user_id', 'screen_name', 'since_id', 'max_id', 'count', 'include_rts', 'trim_user', 'exclude_replies'
    """
    return bind_api(
        api=self,
        path='/statuses/user_timeline.json',
        payload_type='status', payload_list=True,
        allowed_param=['id', 'user_id', 'screen_name', 'since_id',
                       'max_id', 'count', 'include_rts', 'trim_user',
                       'exclude_replies']
    )
