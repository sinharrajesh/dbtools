#!/usr/bin/python

import json
import logging
import sys
from datetime import datetime

   

if __name__ == '__main__':

    with open(sys.argv[1]) as dataFile:
        for line in dataFile:
            data = json.loads(line)

            id_str = data["id_str"]
            print("%s" %(id_str))
