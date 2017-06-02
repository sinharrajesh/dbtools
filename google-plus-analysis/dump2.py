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
import pandas as pd

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
    USAGE = "dump2.py gpostfile altfile"
    if len(argv) != 3:
        logger.error("Valid URL not supplied to script. Usage is %s", USAGE)
        return False

def readGpostFile(filename):
    column_name = ['dateP','timeP', 'id', 'title', 'in_altmetric', 'url', 'verb', 'authorDisplayName', 'authorId', 'authorUrl','objectId', 'objectAuthorId','objectAuthorDisplayName','objectContent']
    df1 = pd.read_csv(filename, sep='$', header=None, names=column_name)
    return df1

def readAltFile(filename):
    column_name = ['authorDisplayName','id', 'dateP', 'timeP', 'summary', 'homepage']
    df2 = pd.read_csv(filename, sep='$', header=None, names=column_name)
    return df2

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    if checkUsage(*sys.argv) is False:
        sys.exit(1)

    gpostFile = sys.argv[1]
    altfile = sys.argv[2]
    gdf = readGpostFile(gpostFile)
    adf = readAltFile(altfile)
    #altmetricOp = pd.DataFrame(adf.groupby( ['authorDisplayName','homepage']).size().sort_values(ascending=False).rename('postCounts'))
    #gpostop     = pd.DataFrame(gdf.groupby( ['authorDisplayName','authorUrl']).size().sort_values(ascending=False).rename('postCounts'))
    altmetricOp = adf.groupby(['authorDisplayName','homepage']).agg({'dateP': len}).rename(columns = {'dateP':'posts'})
    altmetricOp.to_csv('altmetricgb.csv', sep="$", header=True)
    gpostop = gdf.groupby(['authorDisplayName','authorUrl']).agg({'dateP': len}).rename(columns = {'dateP':'posts'})
    gpostop.to_csv('gpostgb.csv', sep="$", header=True)
    print altmetricOp
    print gpostop
