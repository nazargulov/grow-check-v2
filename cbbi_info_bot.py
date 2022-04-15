#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""



"""

pip3
pip3 install requests
pip3 install selenium
brew install chromedriver --cask

"""

import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, ForceReply
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown

import requests
import time
from datetime import datetime, timezone, timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

driver = webdriver.Chrome("chromedriver")


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def send_result():
    url = "https://colintalkscrypto.com/cbbi/"
    driver.get(url)
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    time.sleep(10)

    value = driver.find_element(by=By.CLASS_NAME, value="confidence-score-value")
    return value.text

def check(update: Update, context: CallbackContext) -> None:
    value = send_result()
    update.message.reply_text('CBBI.info: ' + value)

def echo(update: Update, context: CallbackContext) -> None:
    value = send_result()
    update.message.reply_text('CBBI.info: ' + value)

def callback_day(context: CallbackContext):
    value = send_result()
    context.bot.send_message(chat_id='-1001316956052', text='CBBI info: ' + value)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5290196846:AAETI6HGS0FzQriQZvhSZFEpOzpzpnntNus")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cbbi", check))

    job = updater.job_queue
    delta, now = 2, datetime.now(timezone.utc)
    time_of_day = (now + timedelta(seconds=delta)).time()
    job.run_daily(callback_day, time_of_day)
    #job.run_once(callback_day, 1)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
