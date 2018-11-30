from twipy.api import TwitterAPI
import twipy.config as config
import pandas as pd
import json


if __name__ == "__main__":
    api = TwitterAPI(
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token=config.ACCESS_TOKEN,
        access_secret=config.ACCESS_SECRET
    )
    api.user_timeline_params = api.set_user_timeline_params(
        count=3200,
        include_rts=False
    )
    res = api.user_timeline()
    tweets = json.loads(res.text)
    header = res.headers
    for key, value in header.items():
        print('{}: {}'.format(key, value))
