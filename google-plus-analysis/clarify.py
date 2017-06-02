#!/usr/bin/python
import json
import logging
import sys
from datetime import datetime
import csv



if __name__ == '__main__':
    _loggingLevel = logging.DEBUG ## How much trace
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    a = {}
    altmetricFile = sys.argv[1]
    with open(altmetricFile) as afData:
        for line in afData:
            data = line.rstrip('\n')
            a[data] = 0


    with open(sys.argv[2], 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='$', quotechar='\'')
        for line in spamreader:
            id = line[0]
            title = line[1]
            url = line[2]
            dateP = line[3]
            restP = line[4]
            actorId = line[5]
            actorUrl = line[6]
            actorDisplayName = line[7]
            verb = line[8]
            objectId = line[9]
            objectActorId = line[10]
            objectActorDisplayName = line[11]
            objectContent = line[12]

            if url not in a.keys():
                in_altmetric = "N"
            else:
                in_altmetric = "Y"

            print("%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%r" %(dateP, restP, id, title, in_altmetric, url, verb, actorDisplayName, actorId, actorUrl, objectId, objectActorId, objectActorDisplayName, objectContent))
