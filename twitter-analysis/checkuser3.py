#!/usr/bin/python

import twitter
import logging
import sys
import pprint

_loggingLevel = logging.INFO
logger = logging.getLogger(__name__)
logging.basicConfig(level=_loggingLevel)

def IterChunks(sequence, chunk_size):
    res = []
    for item in sequence:
        res.append(item)
        if len(res) >= chunk_size:
            yield res
            res = []
    if res:
        yield res  # yield the last, incomplete, portion

def printAll(listx):
    for x in listx:
        print x

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
    consumer_key='D5HBZNyu3ZFALQ37ez2Un5N6t'
    consumer_secret='6VfipEtz5RIArReVvrJ1qVhn3s8avO14cGEJPaRw5ZhHRVvloD'
    access_token_key='75167234-FsCLRSbmvGuoO0QIMo04luQCjMY24kzjqSUlvrRGX'
    access_token_secret='yUwExUANQxrEuqo33XbuwvWXiWoOTE3FuxTLB6dMZP0nh'

    api = twitter.Api(consumer_key=consumer_key,
    		  consumer_secret=consumer_secret,
    		  access_token_key=access_token_key,
    		  access_token_secret=access_token_secret, 
                  sleep_on_rate_limit=True)


    a = []
    altmetricFile = "pp"
    with open(altmetricFile) as afData:
        for line in afData:
            data = line.rstrip('\n')
            a.append(data)
    # Now form chunks of 100 each
    i=0
    b={}
    
    #for screennames in IterChunks(a, 100):
    #    got =[]
    #    logger.info('screennames starting is %d %r', len(screennames), screennames[0])
    #    x = api.UsersLookup(screen_name=screennames, include_entities = False)
    #    for y in x:
    #        got.append(y.screen_name) 
#
#        logger.info('total got is <%d>', len(got))
#        for query in screennames:
#            if query not in got:
##                print query
    for name in ['9999068910','PantulaSwami','Pinkysatsangi1','Premlat_db', 'PuniaIshan','ShubhamSalgotr3','UmmattSimran','gudi1307']:
        logger.info("trying %s,%d",name, i)
        try:
            p = api.GetUser(screen_name=name, include_entities= False)
        except Exception as inst:
            logger.error('Got error in processing %s', name)
            print inst
            pass
