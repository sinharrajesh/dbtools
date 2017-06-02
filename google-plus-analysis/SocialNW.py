#!/usr/bin/python
#
# Author: Rajesh Sinha, Karan Narain
# The base class for Twitter and GPlus Objects
#
import logging
import sys
from bs4 import BeautifulSoup
import urllib2
import re

## Some Important constants 
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_loggingLevel = logging.DEBUG ## How much trace

class AltmetricBase:

    def __init__(self, name, snLink, altmetricId, startPage, endPage):
        self.name = name            # Name of social network
        self.snLink = snLink        # The /twitter or /google link
        self.amUrl  = 'https://www.altmetric.com/details/' + altmetricId + snLink # full link to page1 of social network
        self.startPagination = startPage
        self.endPagination = endPage
        self.baseLink = self.amUrl.replace(self.snLink,'')  # The baselink which is shown when a non-existent page is used
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=_loggingLevel)
        self.logger.debug('Created Altmetric Object')

    def findPosters(self, soup):
        raise NotImplementedError("Subclass must implement abstract method")

    def getMoreSoup(self):
        """ Tries to check all possible links starting from 2 to 1000 and breaks out when 
        we get a redirect. There is no graceful way i.e. HTTP code on redirect when we 
        access a nonexistant link. So we check when almetric returns the base URL of the
        research arcticle and stop then. This is a generator function and keeps returning
        the beautifulsoup of the link 
        """

        # when the list runs out altmteric returns the base url of the research paper
        for a in range(self.startPagination, self.endPagination):
           link = self.amUrl + '/page:' + str(a)
           self.logger.debug('Trying URL - %s', link)
           try:
               page = urllib2.urlopen(link)
               if self.isRedirect(page):
                   self.logger.debug('finishing the generator...')
                   return
               else:
                   self.logger.debug('Yielding Soup')
                   yield BeautifulSoup(page, _parser)
           except urllib2.HTTPError, e:
               self.logger.error('Could not open %s because of HTTP error', link)
               self.logger.error("%r", e.code)
           except urllib2.URLError, e:
               self.logger.error('Could not open %s because of URL error', link) 
               self.logger.error("%r", e.args)

    def isRedirect(self, page):
        return page.geturl() == self.baseLink

    @staticmethod
    def isValidURL(url):
        testUrl  = 'https://www.altmetric.com/details/' + url 
        regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        result = regex.match(testUrl)
        return False if result is None else True

    def openAndLoadURL(self, fname):
        """ Opens the base URL for a network and returns the beautifulSoup through lxml parses """
        self.logger.debug('Opening URL ' + fname)

        try:
           page = urllib2.urlopen(fname)
        except urllib2.HTTPError, e:
           self.logger.error('Could not open ' + fname+ ': HTTP Error ')
           self.logger.error(e.code)
           return False, None
        except urllib2.URLError, e:
           self.logger.error('Could not open ' + fname+ ': URL Error ')
           self.logger.error(e.args)
           return False, None
        soup = BeautifulSoup(page, _parser)
        return True, soup

    def executeAltmetricAnalysis(self):
        posters = []
        status, soup = self.openAndLoadURL(self.amUrl)
        if status:
            posters = self.findPosters(soup)
            self.logger.debug('Found %d posts so far', len(posters))

            for soup in self.getMoreSoup():
                posters.extend(self.findPosters(soup))
                self.logger.debug('Found %d posts so far', len(posters))

            self.logger.info('Found %d posts in total for the link', len(posters))
            posters = list(set(posters))
            self.logger.info('Found %d Unique Posters for the link', len(posters))
            for poster in posters:
                print (poster).encode('utf-8')
            self.logger.info('written all the posters to stdout...')
        else:
            self.logger.error('found error in URL upfront so bailing out')
            sys.stderr.flush()
            sys.stdout.flush()
            sys.exit(1)
