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
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


# Pressing a button on a custom keyboard results in a Message object sent to the bot, which is no different from a 
# regular chat message composed by typing. a Message object gives the flavor chat
# Pressing a button on an inline keyboard results in a CallbackQuery object sent to the bot, which we have to 
# distinguish from a Message object. a CallbackQuery object gives the flavor callback_query

URL="http://www.dayalbagh.org.in/eSatsang/eSatsangIndex.htm"
tinyUrl = 'http://bit.ly'
_parser = "lxml"      ## remember to pip install lxml or else use another parser
_loggingLevel = logging.DEBUG ## How much trace
TOKEN='388622626:AAFRm5IcT5FRVX8ZfT3eZRaPC516Nlggbwg' 

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('got chat message')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='16/5', callback_data='16/5'), 
                    InlineKeyboardButton(text='21/5', callback_data='21/5'),
                    InlineKeyboardButton(text='22/5', callback_data='22/5'),
                    InlineKeyboardButton(text='23/5', callback_data='23/5'),
                    InlineKeyboardButton(text='24/5', callback_data='24/5'),
                    InlineKeyboardButton(text='25/5', callback_data='25/5')]
 
               ])
    bot.sendMessage(chat_id, 'Radhasoami. I have information on following dates. Press the date to get information of transmission schedule for that day', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    text = 'You got details for ' + query_data
    bot.answerCallbackQuery(query_id, text=text)
    print('answered')

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
