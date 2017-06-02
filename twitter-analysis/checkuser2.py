#!/usr/bin/python

import twitter
import logging
import sys
import pprint

_loggingLevel = logging.INFO ## How much trace
logger = logging.getLogger(__name__)
logging.basicConfig(level=_loggingLevel)

def IterChunks(sequence, chunk_size):
    res = []
    for item in sequence:
        res.append(item)
        if len(res) >= chunk_size:
            yield res
            res = []
    if res:
        yield res  # yield the last, incomplete, portion

def printAll(listx):
    for x in listx:
        print x

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
    consumer_key='D5HBZNyu3ZFALQ37ez2Un5N6t'
    consumer_secret='6VfipEtz5RIArReVvrJ1qVhn3s8avO14cGEJPaRw5ZhHRVvloD'
    access_token_key='75167234-FsCLRSbmvGuoO0QIMo04luQCjMY24kzjqSUlvrRGX'
    access_token_secret='yUwExUANQxrEuqo33XbuwvWXiWoOTE3FuxTLB6dMZP0nh'

    api = twitter.Api(consumer_key=consumer_key,
    		  consumer_secret=consumer_secret,
    		  access_token_key=access_token_key,
    		  access_token_secret=access_token_secret)


    a = {}
    altmetricFile = "pp"
    with open(altmetricFile) as afData:
        for line in afData:
            data = line.rstrip('\n')
            a[data] = 0
    # Now form chunks of 100 each
    print api.GetUser(screen_name = sys.argv[1])
