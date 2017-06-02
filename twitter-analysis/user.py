#!/usr/bin/python

import json
import logging
import sys

   

if __name__ == '__main__':
    _loggingLevel = logging.INFO ## How much trace
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    u = {}
    with open(sys.argv[1]) as dataFile:
        for line in dataFile:
            data = json.loads(line)
            id = data["user"]["screen_name"]
            dc = data["user"]["created_at"]
            if 'statuses_count' in data['user']:
                sc = data['user']['statuses_count']
            else:
                sc = 0
            if 'followers_count' in data['user']:
                fc = data['user']['followers_count']
            else:
                fc = 0

            if id not in u.keys():
                u[id ] = list(sc, fc, dc)
                logger.info('id %s added in dict', id)
            else:
                if u[id][0] < sc:
                    u[id] = list(sc, fc, dc)
                else:
                    logger.info('id not added in dict as already there')
