#!/usr/bin/python
# appendpandas allusers.csv alltweets.csv useranalysis (opfile)
import json
import logging
import sys
import csv
import pandas as pd
   

if __name__ == '__main__':
    _loggingLevel = logging.INFO ## How much trace
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    names=['handle','#tweets','#followers','#friends','Joining Date']
    userdf = pd.read_csv(sys.argv[1], header=None, delimiter='$', names = names)
    t_names=['tweetType','handle']
    tweetdf = pd.read_csv(sys.argv[2], header=None, delimiter='$', names=t_names, usecols=[1,4])
    x = pd.pivot_table(tweetdf, index=['handle'], columns=['tweetType'], aggfunc=len, fill_value=0)
    x = x.reset_index()
    summary = pd.merge(x, userdf, how='left', left_on=['handle'], right_on=['handle'])
    summary['Total'] = summary['Reply'] + summary['Tweet'] + summary['Retweet']
    summary['n-cubit related %age'] = summary['Total']/summary['#tweets']
    summary.reindex(columns=['handle','Tweet','Retweet','Reply','Total','#tweets','#followers','#friends','Joining Date','n-cubit related %age']).to_csv(sys.argv[3], index=False)
