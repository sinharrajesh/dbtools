#!/usr/bin/python
#
# Author: Rajesh Sinha, Karan Narain
# Usage: twitter.py <altmetric gplus url>
#        e.g. twitter.py https://www.altmetric.com/details/19547688/twitter user|tweet
#        e.g. twitter.py https://www.altmetric.com/details/19547688/twitter > op.csv
#        It outputs the twitterhandle:Name of Twitter separated by : if you give user on command line
#        It will output the tweet id (i.e. the status id_str in twitter terms if you give tweet on command line
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
        USAGE = "twitter.py altmetricId user|tweet"
        if len(argv) != 3:
            logger.error("Valid URL not supplied to script. Usage is %s", USAGE)
            return False
        else:
            validUrl = AltmetricBase.isValidURL(argv[1])
        return True


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

    def findTweets(self, soup):
        tHandle = [] 
        timeTag = soup.find_all("time")
        for tt in timeTag:
            aTag    = tt.find_all("a")
            for a in aTag:
                tweetId = a.get('href').split('/')[5]
                tHandle.append(tweetId)
        return  tHandle

    def listAllTweets(self):
        tweets = []
        status, soup = self.openAndLoadURL(self.amUrl)
        if status:
            tweets = self.findTweets(soup)
            self.logger.debug('Found %d posts so far', len(tweets))

            for soup in self.getMoreSoup():
                tweets.extend(self.findTweets(soup))
                self.logger.debug('Found %d posts so far', len(tweets))

            self.logger.info('Found %d posts in total for the link', len(tweets))
            tweets = list(set(tweets))
            self.logger.info('Found %d Unique tweets for the link', len(tweets))
            for tweet in tweets:
                print (tweet).encode('utf-8')
            self.logger.info('written all the tweets to stdout...')
        else:
            self.logger.error('found error in URL upfront so bailing out')
            sys.stderr.flush()
            sys.stdout.flush()
            sys.exit(1)


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    if Twitter.checkUsage(*sys.argv) is False:
        sys.exit(1)

    fname = sys.argv[1]
    if sys.argv[2] == "user":
        tw = Twitter("Twitter", socialMediaURL, fname, _startPagination, _endPagination)
        tw.executeAltmetricAnalysis()
    else:
        tw = Twitter("Twitter", socialMediaURL, fname, _startPagination, _endPagination)
        tw.listAllTweets()
