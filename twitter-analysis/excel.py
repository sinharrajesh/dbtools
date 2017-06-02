#!/usr/bin/python

import json
import logging
import sys
from datetime import datetime

   

if __name__ == '__main__':

    with open(sys.argv[1]) as dataFile:
        for line in dataFile:
            data = json.loads(line)

            id_str = data["id_str"]
            cr_dt  = data["created_at"]
            cr_dt  = cr_dt.replace("+0000 ", "")
            hash = ""
            if 'hashtags' in data.keys():
                hashes   = data["hashtags"]

            rt_cnt = 0
            if 'retweet_count' in data.keys():
                rt_cnt = data["retweet_count"]

            rt_status = ""
            rt_from   = ""
            if 'retweeted_status' in data.keys():
                rt_status = data["retweeted_status"]
                rt_from   = data["retweeted_status"]["user"]["screen_name"]

            text = data["text"]
            user = data["user"]["screen_name"]

            st_cnt = 0
            if 'statuses_count' in data['user']:
                st_cnt = data["user"]["statuses_count"]

            fc_cnt = 0
            if 'followers_count' in data['user']:
                fc_cnt = data["user"]["followers_count"]

            fr_cnt = 0
            if 'friends_count' in data['user']:
                fr_cnt = data["user"]["friends_count"]  

            print("%s$%s$%s$%s$%r$%s$%s$%s$%s$%r$%r" %(id_str, cr_dt, user, rt_cnt, st_cnt, fc_cnt, fr_cnt, rt_from, hash, text, rt_status))
