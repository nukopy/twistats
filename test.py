import twipy.config as config
from twipy.api import TwitterAPI
import sys
sys.path.append('twipy')

if __name__ == "__main__":
    api = TwitterAPI(
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_secret=config.ACCESS_SECRET
    )
