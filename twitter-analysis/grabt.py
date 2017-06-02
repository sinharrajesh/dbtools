#!/usr/bin/python

import twitter
import logging
import sys

_loggingLevel = logging.INFO ## How much trace
logger = logging.getLogger(__name__)
logging.basicConfig(level=_loggingLevel)


def printAll(listx):
    for x in listx:
        printTweet(x)

def printTweet(x):
    if x.tweet_mode == 'extended':
        text = x.full_text
    else:
        text = x.text
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


    term = 'http://www.tandfonline.com/doi/full/10.1080/03081079.2017.1308361'
    lastId = int(sys.argv[1])

    continueLoop = True
    tweets = []
    while continueLoop:
        logger.info('**** lastId is <%d> *****', lastId)
        lastId = lastId + 1
        logger.info('**** Incremented Value is %d', lastId)
        x = api.GetSearch(term = term, since_id = lastId, count=30000, include_entities=True)
        for y in x:
    	    lastId = y.id 
    	    tweet = y
    	    tweets.append(tweet)

        logger.info("************ TOTAL COUNT IS %d", len(tweets))
        if len(x) < 100:
           continueLoop = False 
           logger.info("coming out of the loop as last count is <100")

    printAll(tweets)
