#!/usr/bin/python

import twitter
import logging
import sys

_loggingLevel = logging.INFO ## How much trace
logger = logging.getLogger(__name__)
logging.basicConfig(level=_loggingLevel)


def printAll(listx):
    for x in listx:
        print x

if __name__ == '__main__':
    consumer_key='D5HBZNyu3ZFALQ37ez2Un5N6t'
    consumer_secret='6VfipEtz5RIArReVvrJ1qVhn3s8avO14cGEJPaRw5ZhHRVvloD'
    access_token_key='75167234-FsCLRSbmvGuoO0QIMo04luQCjMY24kzjqSUlvrRGX'
    access_token_secret='yUwExUANQxrEuqo33XbuwvWXiWoOTE3FuxTLB6dMZP0nh'

    api = twitter.Api(consumer_key=consumer_key,
    		  consumer_secret=consumer_secret,
    		  access_token_key=access_token_key,
    		  access_token_secret=access_token_secret)


    term = sys.argv[1]
    sinceId = int(sys.argv[2])

    if len(sys.argv) == 4:
        lastId = int(sys.argv[3])
    else:
        lastId = 100000000000000000000

    continueLoop = True
    tweets = []
    while continueLoop:
        tillId = lastId - 1
        logger.info('operating range is <%d> - <%d>', tillId, sinceId)
        x = api.GetSearch(term = term, result_type ='recent', max_id = tillId, since_id = sinceId, count=30000, include_entities=True)
        for y in x:
    	    lastId = y.id 
    	    tweet = y
    	    tweets.append(tweet)

        logger.info("************ TOTAL COUNT IS %d", len(tweets))
        if len(x) < 100:
           continueLoop = False 
           logger.info("coming out of the loop as last count is <100")

    printAll(tweets)
