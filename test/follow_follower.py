#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import pandas as pd
import json
import time
import config
import agent

"""
-- Refference --
http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-friends-ids.cgi
"""


class FF(agent.Agent):
    def get_ff(self, url_ff, user_id, cursor=-1, count=200):
        """
        Assigned a userID(screen_name such as mathnuko),
        and get user's follower-id and number
        -- arguments --
        :user_id: str
        :cursor: int(default -1 means first page)
        :count: int(default 200 means the max number of users you can get per page)
        """
        # request
        req_count = 0
        params = {
            "screen_name": user_id,
            "cursor": cursor,
            "stringify_ids": True,
            "count": count,
            "skip_status": True
        }
        # response of HTTP request
        res = self.api.get(url=url_ff, params=params)
        req_count += 1

        # result
        max_request_per15sec = 15
        if res.status_code == 200:
            json_obj = json.loads(res.text)  # all tweets info
            print(json_obj)
            name_ff = [[user["screen_name"],
                        user["friends_count"],
                        user["followers_count"]] for user in json_obj["users"]]  # user=dict

            # When followers of user is 5000 or more, enter this block.
            while json_obj["next_cursor"] > 0:
                # update params property
                params["cursor"] = json_obj["next_cursor"]
                res = self.api.get(url=url_ff, params=params)  # request again
                json_obj = json.loads(res.text)
                print(json_obj)
                name_ff += [[user["screen_name"],
                             user["friends_count"],
                             user["followers_count"]] for user in json_obj["users"]]  # stack
                req_count += 1
                if req_count == max_request_per15sec:
                    print("Requests count reached max.\nPlease wait 15 min(900sec).")
                    req_count = 0
                    time.sleep(900)  # 10sec 15*60

            # output
            for user in json_obj["users"]:
                print("-" * 10)
                print("user_name:", user["screen_name"])
                print("follow:", user["friends_count"])
                print("follower:", user["followers_count"])

        else:
            print("ERROR!: {}".format(res.status_code))
            name_ff = []

        return name_ff


if __name__ == '__main__':
    """
    e.g.)
    # id = "physics303"
    # id = "yousuck2020"
    # id = "Hal_Tasaki"
    # url_follows = "https://api.twitter.com/1.1/friends/list.json"
    # id_follows, num_follows = ff.get_ff(url_follows, id)
    """
    # constant
    id_ac = "mathnuko"
    url_followers = "https://api.twitter.com/1.1/followers/list.json"
    pd_columns = ["user_name", "follow", "follower"]

    # class-declaration
    ff = FF()
    username_ff = ff.get_ff(url_followers, id_ac)
    df = pd.DataFrame(data=username_ff, columns=pd_columns)
    df["follow-follower Rate"] = (df["follow"] /
                                  df["follower"] * 100).map(int).map(str) + " %"
    df.to_csv("output/my_ff_data.csv", encoding="utf-8")
