#!/usr/bin/python
#
# Author: Rajesh Sinha, Karan Narain
# Usage: twitter.py <altmetric gplus url>
#        e.g. twitter.py https://www.altmetric.com/details/19547688/twitter
#        e.g. twitter.py https://www.altmetric.com/details/19547688/twitter > op.csv
#        It outputs the twitterhandle:Name of Twitter separated by :
#        from altmetric 

import logging
import sys
from bs4 import BeautifulSoup
import urllib2
from SocialNW import AltmetricBase

## Some Important constants 
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_startPagination = 2  ## altmetric url appends www.altmetric.com/{details/{ResPaperNo}/{socNw}/page:{} 
_endPagination = 1000 ## maximum pages to search starting from _startPagination
socialMediaURL = "/twitter" ## what gets appended at the end of altmetricURL for twitter
_loggingLevel = logging.DEBUG ## How much trace

class Twitter(AltmetricBase):
    def __init__(self, name, snLink, altmetricUrl, startPage, endPage):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=_loggingLevel)
        AltmetricBase.__init__(self, name, snLink, altmetricUrl, startPage, endPage)
        self.logger.debug('Created %s Object', self.name)

    @staticmethod
    def checkUsage(*argv):
        USAGE = "twitter.py altmetricId"
        if len(argv) != 2:
            logger.error("Valid URL not supplied to script. Usage is %s", USAGE)
            return False
        else:
            validUrl = AltmetricBase.isValidURL(argv[1])
            if validUrl:
                return True
            else:
                logger.error('URL supplied <%s> is invalid', argv[1])
                return False


    def findPosters(self, soup):
        authorTag = soup.find_all("div", {"class": "author"})
        tHandle = []
        for author in authorTag:
    	    nameTag = author.find_all("div", {"class": "name"})
    	    handleTag = author.find_all("div", {"class": "handle"})
    	    name = nameTag[0].text
    	    handle = handleTag[0].text
    	    toAdd = handle + ":" + name
    	    tHandle.append(toAdd)
        return tHandle


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    if Twitter.checkUsage(*sys.argv) is False:
        sys.exit(1)

    fname = sys.argv[1]
    tw = Twitter("Twitter", socialMediaURL, fname, _startPagination, _endPagination)
    tw.executeAltmetricAnalysis()
