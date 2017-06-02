#!/usr/bin/python
# Author: Rajesh Sinha, Karan Narain
# Usage: botrating.py useranalys0106.csv Opfilename endingAt startingfrom keyfile
#        useranalysis0106.csv is the supplied file which has prelim user data
#        opfilename is the name the script will write to
#        endingAt at which row
#        starting from which row. 
#        key-file has mashape and 4 twitter keys
# Now we can run this in chunks of 1000 as follows
#        botrating.py useranalysis0106.csv first1000.csv 1000   1
#        botrating.py useranalysis0106.csv second1000.csv 2000   1001
#        botrating.py useranalysis0106.csv third1000.csv 3000   2001
#        botrating.py useranalysis0106.csv fourth1000.csv 4000   3001
#        ...
#        botrating.py useranalysis0106.csv last1000.csv 10000   9001
#  Note it will be useful to redirect the stdout to a file so that in case things go wrong
#  you still have the output for the records processed which can be manually merged
# 
#        botrating.py useranalysis0106.csv first1000.csv 1000   1 > first1000.tmp 
#        do not redirect the stderr
#
import botometer
import logging
import random
import pandas as pd
import sys

#logging level
_loggingLevel = logging.INFO ## How much trace

def connectToBoto(mashape_key, consumer_key, consumer_secret, access_token_key, access_token_secret):
    twitter_app_auth = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'access_token': access_token_key,
        'access_token_secret': access_token_secret,
      }

    try:
        bom = botometer.Botometer(mashape_key=mashape_key, **twitter_app_auth)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        logger.error('Unexpected error: %r', sys.exc_info()[0])
        logger.error('Exception in connecting to Boto Mashape Gateway or Twitter')
        return None

    return bom

def openCsvFile(filename, startIndex, endAt):
    logger.info('Passed params %s %d %d', filename, startIndex, endAt)
    # Read the input file useranalysis0106.csv or whatever
    df = pd.read_csv(sys.argv[1]) # Read all rows as for some reasons lambda is not working
    logger.info('Subsetting the dataframe %r at %d:%d', df.shape, startIndex-1, endAt)
    df = df[startIndex -1:endAt]

    # Add the scores related columns to dataframe with default valuesO
    # If you set anything to 0 you will always get 0 as column gets int
    # type and all botometer returns are <0 decimals

    df['ID String'] = ''
    df['Score-English'] = 0.0
    df['Score-Universal'] = 0.0
    df['Score-Network'] = 0.0
    df['Score-Content'] = 0.0
    df['Score-Sentiment'] = 0.0
    df['Score-Temporal'] = 0.0
    df['Score-Friend'] = 0.0
    df['Score-User'] = 0.0

    #return the data frame
    return df

    
def checkBotRatings(df):
    # Iterate over the dataframe - passing handle to botometer and updating bot scores
    for i, row in df.iterrows():
        name = row['handle']
        try:
            result = bom.check_account(name)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass
        id_str = ''
        nw = 0
        cn = 0
        sn = 0
        tm = 0
        fr = 0
        us = 0
        sc_en = 0
        sc_un = 0
        if 'user' in result:
            if 'id_str' in result['user']:
                id_str = result['user']['id_str']
                nw     = result['categories']['network']
                cn     = result['categories']['content']
                sn     = result['categories']['sentiment']
                tm     = result['categories']['temporal']
                fr     = result['categories']['friend']
                us     = result['categories']['user']
                sc_en  = result['scores']['english']
                sc_un  = result['scores']['universal']
                df.set_value(i,'ID String', id_str)
                df.set_value(i,'Score-English' , sc_en)
                df.set_value(i,'Score-Universal' , sc_un)
                df.set_value(i,'Score-Network' , nw)
                df.set_value(i,'Score-Content' , cn)
                df.set_value(i,'Score-Sentiment' , sn)
                df.set_value(i,'Score-Temporal' , tm)
                df.set_value(i,'Score-Friend' , fr)
                df.set_value(i,'Score-User' , us)
        print("%s,%s,%r,%r,%r,%r,%r,%r,%r,%r" %(name, id_str, sc_en, sc_un, nw, cn, sn, tm, fr, us))
        sys.stdout.flush()
    return df

def writeToOutputFile(df, opfilename):
    # write back to a csv file post reordering of columns in the way we want 
    df.reindex(columns=['handle','ID String','Tweet','Retweet','Reply','Total','#tweets','#followers','#friends','Joining Date','n-cubit related %age', 'Score-English', 'Score-Universal', 'Score-Network','Score-Content', 'Score-Sentiment','Score-Temporal','Score-Friend','Score-User']).to_csv(opfilename, index=False)
    return

def checkUsage(*argv):
    USAGE="botrating.py inputfile opfile endAt rowstostartat keyfile"
    if len(argv) != 6:
        logger.error("Invalid No of arguments. Usage is %s", USAGE)
        return (False, None, None, None, None, None)
    else:
        try:
            inputFile = sys.argv[1]
            outputFile = sys.argv[2]
            endAt  = int(sys.argv[3])
            rowsToStartAt  = int(sys.argv[4])
            keyfile = sys.argv[5]
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            logger.error('Unexpected error: %r', sys.exc_info()[0])
            logger.error("Invalid arguments. Usage is %s", USAGE)
            return (False, None, None, None, None, None)
    return (True, inputFile, outputFile, endAt, rowsToStartAt, keyfile)


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    status, inputFile, outputFile, endAt, rowsToStartAt,keys = checkUsage(*sys.argv)
    if status is False:
        sys.exit(1) 

    keyfile = __import__(keys)
    bom = connectToBoto(keyfile.mashape_key, keyfile.consumer_key, keyfile.consumer_secret, keyfile.access_token_key, keyfile.access_token_secret)
    if bom:
        df = openCsvFile(inputFile, rowsToStartAt, endAt)
        df1 = checkBotRatings(df)
        writeToOutputFile(df1, outputFile)
        sys.exit(0)
    else:
        logger.error('Unable to connect to Boto and Twitter')
        sys.exit(1)
