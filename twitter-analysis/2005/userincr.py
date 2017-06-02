#!/usr/bin/python

import json
import logging
import sys
import csv
   

if __name__ == '__main__':
    _loggingLevel = logging.INFO ## How much trace
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=_loggingLevel)

    u = {}
    with open(sys.argv[1], 'rb') as csvfile:
        opreader = csv.reader(csvfile, delimiter='$', quotechar='|')
        for data in opreader:
            id = data[4]
            sc = int(data[5])
            fc = int(data[6])
            fr = int(data[7])
            cr = data[15]
            if id not in u.keys():
                u[id] = [sc, fc, fr, cr]
            else:
                if u[id][0] < sc:
                    u[id] = [sc, fc, fr, cr]
                else:
                    pass

    for key, value in u.items():
        print("%s$%d$%d$%d$%s" %(key, value[0],value[1],value[2], value[3]))
