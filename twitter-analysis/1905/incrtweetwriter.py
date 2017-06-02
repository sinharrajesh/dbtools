#!/usr/bin/python

import json
import logging
import sys

   
def printall(tweets):


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    df = sys.argv[1]
    cf = sys.argv[2]

    c = {}
    with open(cf) as commonFile:
        for line in commonFile:
            c[int(line)] = 0

    tweets = []
    with open(sys.argv[1]) as dataFile:
        for line in dataFile:
            data = json.loads(line)
            if data["id"] in c.keys():
                logger.info('The key %d already exists in common file not to be written')
            else:
                tweets.append(data)

    for tweet in tweets:
        print tweet
