#!/usr/bin/python

import json
import logging
import sys
from datetime import datetime
import XlsxWriter

   

if __name__ == '__main__':
    _loggingLevel = logging.DEBUG ## How much trace
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    c = {}
    commonFile = sys.argv[2]
    with open(commonFile) as cfData:
        for line in cfData:
            c[int(line)] = 0

    with open(sys.argv[1]) as dataFile:
        for line in dataFile:
            data = json.loads(line)

            id_str = data["id_str"]
            if int(id_str) not in c.keys():
    	        cr_dt  = data["created_at"]
    	        cr_dt  = cr_dt.replace("+0000 ", "")
    	        hashes = ''
    	        if 'hashtags' in data.keys():
    		    hashes   = data["hashtags"]

    	        rt_cnt = 0
    	        if 'retweet_count' in data.keys():
    		    rt_cnt = data["retweet_count"]

                tweet_type = "Tweet"
    	        rt_status = ''
    	        rt_from   = ''
    	        if 'retweeted_status' in data.keys():
    		    rt_status = data["retweeted_status"]
    		    rt_from   = data["retweeted_status"]["user"]["screen_name"]
                    tweet_type = "Retweet"

                reply_to = ''
                reply_to_status = ''
                if 'in_reply_to_screen_name' in data.keys():
                    reply_to  = data['in_reply_to_screen_name']
                    tweet_type = "Reply"
                if 'in_reply_to_status_id' in data.keys():
                    reply_to_status = data['in_reply_to_status_id']

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

    	        print("%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%r$%r$%r$%s" %(id_str, tweet_type, cr_dt, user, st_cnt, fc_cnt, fr_cnt, rt_cnt, rt_from, reply_to, hashes, text, rt_status, reply_to_status))
