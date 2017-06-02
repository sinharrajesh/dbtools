#!/usr/bin/python
import logging
import sys
from bs4 import BeautifulSoup
import urllib2
import re
import pytz
from datetime import datetime, date
import time
import telepot
from telepot.loop import MessageLoop


URL="http://www.dayalbagh.org.in/eSatsang/eSatsangIndex.htm"
tinyUrl = 'http://bit.ly'
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_loggingLevel = logging.DEBUG ## How much trace
TOKEN='388622626:AAFRm5IcT5FRVX8ZfT3eZRaPC516Nlggbwg' 

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
