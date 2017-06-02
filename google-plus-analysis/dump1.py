#!/usr/bin/python
#
# Author: Rajesh Sinha, Karan Narain
#        from altmetric 

import logging
import sys
from bs4 import BeautifulSoup
import urllib2
import re
import config
from apiclient import discovery
import json

## Some Important constants 
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_startPagination = 2  ## altmetric url appends www.altmetric.com/{details/{ResPaperNo}/{socNw}/page:{} 
_endPagination = 1000 ## maximum pages to search starting from _startPagination
socialMediaURL = "/twitter" ## what gets appended at the end of altmetricURL for twitter
_loggingLevel = logging.DEBUG ## How much trace
API_KEY = config.APIKEY

def isValidURL(url):
    regex = re.compile(
	    r'^(?:http|ftp)s?://' # http:// or https://
	    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
	    r'localhost|' #localhost...
	    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	    r'(?::\d+)?' # optional port
	    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    result = regex.match(url)
    return False if result is None else True

def checkUsage(*argv):
    USAGE = "dumpgpost.py url"
    if len(argv) != 2:
        logger.error("Valid URL not supplied to script. Usage is %s", USAGE)
        return False

def printPost(item):
    id = item['id']
    title = item['title']
    url = item['url']
    published = item['published']
    dateP = published.split("T")[0]
    restP = published.split("T")[1]
    actorId = item['actor']['id']
    actorUrl = item['actor']['url']
    actorDisplayName = item['actor']['displayName']
    verb = item['verb']
    objectContent = ''
    objectOriginalContent = ''
    objectId = ''
    objectActorId = ''
    objectActorDisplayName = ''
    if 'object' in item:
        if 'content' in item['object']:
            objectContent = item['object']['content']
        if 'originalContent' in item['object']:
            objectOriginalContent = item['object']['originalContent']
        objectType = item['object']['objectType']
        if 'id' in item['object']:
            objectId = item['object']['id']
        if 'actor' in item['object']:
            if 'id' in item['object']['actor']:
                objectActorId = item['object']['actor']['id']
            if 'displayName' in item['object']['actor']:
                objectActorDisplayName = item['object']['actor']['displayName']

#    print("%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%s$%r" %( id, title, url, dateP, restP, actorId, actorUrl, actorDisplayName, verb, objectId, objectActorId, objectActorDisplayName, objectContent))
#    print("%r$%r$%r$%r$%r$%r$%r$%r$%r$%r$%r$%r" %( id, title, url, published, actorId, actorUrl, actorDisplayName, verb, objectId, objectActorId, objectActorDisplayName, objectContent))
    print("%r$%r$%r$%r$%r$%r$%r$%r$%r$%r$%r$%r$%r" %( unicode(id), unicode(title), unicode(url), unicode(dateP), unicode(restP), unicode(actorId), unicode(actorUrl), unicode(actorDisplayName), unicode(verb), unicode(objectId), unicode(objectActorId), unicode(objectActorDisplayName), unicode(objectContent)))

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    if checkUsage(*sys.argv) is False:
        sys.exit(1)

    fname = sys.argv[1]


    GPLUS = discovery.build('plus', 'v1', developerKey=API_KEY)
    continueLoop = True
    pageToken = None
    prevToken = ""
    totalP = 0
    while continueLoop:
        response = GPLUS.activities().search(query=fname, maxResults=20, orderBy="recent", pageToken=pageToken).execute()
        if 'items' in response:
            totalItems = len(response['items'])
            totalP = totalP + totalItems
            continueLoop = False if totalItems == 0 else True
            logger.info('Total Items = <%d>', totalItems)
            for item in response['items']:
                printPost(item)
        prevToken = pageToken if pageToken else ''
        pageToken = response['nextPageToken']
        if pageToken or pageToken == '':
            print('Got PageToken')
            continueLoop = True
        else:
            print('NOOOOO PageToken')
            continueLoop = False
    logger.info('Total Posts <%d> for <%s>', totalP, fname)
