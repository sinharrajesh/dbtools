#!/usr/bin/python
# 388622626:wq
# Author: Rajesh Sinha, Karan Narain
# The base class for Twitter and GPlus Objects
#
import logging
import sys
from bs4 import BeautifulSoup
import urllib2
import re
import pytz
from datetime import datetime, date, time


URL="http://www.dayalbagh.org.in/eSatsang/eSatsangIndex.htm"
tinyUrl = 'http://bit.ly'
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_loggingLevel = logging.DEBUG ## How much trace

schedule = []
scheduleFetched = None

def convertTimesToDatetimeInIST(date1, time1):
    #make a datetime object with assumption that year is current year 
    curDay = date1.split('/')[0].zfill(2)
    curMth = date1.split('/')[1].zfill(2)
    timePart = time1.split(' ')[0]
    amPm     = time1.split(' ')[1].upper()
    hrs      = timePart.split(':')[0].zfill(2)
    min      = timePart.split(':')[1].zfill(2) + ':00'
    timeFormat = '%d/%m/%Y %I:%M:%S %p'
    dt_string = curDay + '/' + curMth + '/' + str(date.today().year) + ' ' + hrs + ':' + min + ' ' + amPm
    logger.debug('Date string is <%s>', dt_string)
    istMomentNaive = datetime.strptime(dt_string, timeFormat)
    logger.debug('Date string is <%r>', istMomentNaive)
    return istMomentNaive

def ParseSite(url, mode):
    if mode == 'online':
        status, soup = openAndLoadURL(url)
    else:
        status, soup = loadFromFile(url)
    #check that we are good for parsing this properly
    #There should be three MsoNormalTable in this
    tables = soup.find_all('table', {'class' : 'MsoNormalTable'})
    if len(tables) != 3:
        msg= 'Something is not right in DB Site page. Please check this link manually ' + tinyUrl   
        return False, msg


    schedule = []
    schTable = tables[1] 
    firstRow = True
    prevDt = ""
    prevOccasion = ""
    for row in schTable.find_all('tr'):
        if not firstRow:
            allCols = row.find_all('td')
            logger.debug('Len of cols is %d', len(allCols))
            if len(allCols) == 4:
                dt = prevDt
                occasion = prevOccasion
                colData = []
                for data in allCols:
                    colData.append(findColData(data))

                details = colData[0]
                cascade = colData[1]
                stTime  = colData[2]
                scTime  = colData[3]
            else:
                colData = []
                for data in allCols:
                    colData.append(findColData(data))

                dt      = colData[0]
                occasion= colData[1]
                details = colData[2]
                cascade = colData[3]
                stTime  = colData[4]
                scTime  = colData[5]
                prevDt = dt
                prevOccasion = occasion
            dtIstst = convertTimesToDatetimeInIST(dt, stTime)
            dtIstct = convertTimesToDatetimeInIST(dt, stTime)
            schedule.append([dt, occasion, details, cascade, stTime, scTime, dtIstst, dtIstct])
        firstRow = False

    for row in schedule:
        logger.debug("<%s>-<%s>-<%s>-<%s>-<%s>-<%s>", row[0], row[1], row[2], row[3], row[4], row[5])
    return True, None

def findColData(data):
    all_data = []
    for writing in data.find_all('span'):
        all_data.append(re.sub('\s\s+', ' ', writing.text.lstrip()))
    return(' '.join(all_data))
    
    
def findSchedule():
    pass

def loadFromFile(fname):
    soup = BeautifulSoup(open(fname), _parser)
    return True, soup

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)
    
    USAGE = "esatsang.py online|name of file"
    if len(sys.argv) != 2:
        logger.error("Valid URL not supplied to script. Usage is %s", USAGE)
        sys.exit(-1)
    else:
        opt  = sys.argv[1]
        ParseSite(opt, opt)
