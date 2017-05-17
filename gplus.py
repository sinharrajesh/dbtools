#!/usr/bin/python
#
# Author: Rajesh Sinha, Karan Narain
# Usage: gplus.py <altmetric gplus url>
#        e.g. gplus.py https://www.altmetric.com/details/19547688/google
#        e.g. gplus.py https://www.altmetric.com/details/19547688/google > op.csv
#
# This dumps the Google+ Id or the Name as available in the Google Plus Page of
# the poster for a ALTMETRIC tracked publication 
# as collected by altmetric

import logging
import sys
from bs4 import BeautifulSoup
import urllib2
from SocialNW import AltmetricBase

## Some Important constants 
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_startPagination = 2  ## altmetric url appends www.altmetric.com/{details/{ResPaperNo}/{socNw}/page:{} 
_endPagination = 1000 ## maximum pages to search starting from _startPagination
socialMediaURL = "/google" ## what gets appended at the end of altmetricURL for twitter
_loggingLevel = logging.DEBUG ## How much trace

class GPlus(AltmetricBase):
    def __init__(self, name, snLink, altmetricUrl, startPage, endPage):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=_loggingLevel)
        AltmetricBase.__init__(self, name, snLink, altmetricUrl, startPage, endPage)
        self.logger.debug('Created %s Object', self.name)

    @staticmethod
    def checkUsage(*argv):
        USAGE = "gplus.py altmetricId"
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
        tHandle = []
        postTag = soup.find_all("article", {"class" : "post gplus"})
        # find the Google Plus Id if available from href
        for post in postTag:
           gplusId = "+_unknown"
           aTag = post.find_all("a", {"class": "block_link" })
           for a in aTag:
               y =  a.get('href').split(u'/')[3]
               if y and y[0] == '+':
                   gplusId = y
               else:
                   img = a.find('img')
                   if img:
                       gmailName = img.get('alt')
                       if gmailName and len(gmailName) > 0:
                           gplusId = gmailName
               if gplusId  == "+_unknown":
                   gplusUrl = 'https://plus.google.com/' + y
                   try:
                       gpage = urllib2.urlopen(gplusUrl)
                       gpageSoup = BeautifulSoup(gpage, _parser)
                       gpageTitle = gpageSoup.title.string
                       gplusId = gpageTitle.replace(" - Google+","")
                   except urllib2.HTTPError, e:
                       self.logger.debug('Could not open %s because of HTTP error', gplusUrl)
                       self.logger.debug("%r", e.code)
                       self.logger.debug("Original Tag %r", a)
                   except urllib2.URLError, e:
                       self.logger.debug('Could not open %s because of URL error', gplusUrl) 
                       self.logger.debug("%r", e.args)
                       self.logger.debug("Original Tag %r", a)
               tHandle.append(gplusId)

        return tHandle


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    if GPlus.checkUsage(*sys.argv) is False:
        sys.exit(1)

    articleId = sys.argv[1]
    gp = GPlus("GPlus", socialMediaURL, articleId, _startPagination, _endPagination)
    gp.executeAltmetricAnalysis()
