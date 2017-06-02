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
            id = data[0]
            sc = data[1]
            fc = data[2]
            fr = data[3]
            cr = data[4]
            if id not in u.keys():
                u[id] = [sc, fc, fr, cr]

    logger.info('Total loaded is %d', len(u))

    with open(sys.argv[2], 'rb') as csvfile:
        opreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for data in opreader:
            id = data[0]
            tw = data[1]
            rt = data[2]
            rp = data[3]
            bb = data[4]
            gt = data[5]
            if id in u.keys():
                sc = u[id][0]
                fc = u[id][1]
                fr = u[id][2]
                cr = u[id][3]
                print("%s,%s,%s,%s,%s,%s,%s,%s,%s" %(id, tw, rt, rp, gt, sc, fc, fr, cr))
            else:
                print("%s,%s,%s,%s,%s,%s,%s,%s,%s" %(id, tw, rt, rp, gt, "", "", "", ""))
