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

pip install PyVirtualDisplay
3
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import requests
import time
from datetime import datetime, timezone

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# https://blog.testproject.io/2018/02/20/chrome-headless-selenium-python-linux-servers/
#install Xvfb
#sudo apt-get install xvfb

#set display number to :99
#Xvfb :99 -ac &
#export DISPLAY=:99

# Option 1 - with ChromeOptions
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
#driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options,
#  service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
# Option 2 - with pyvirtualdisplay
#from pyvirtualdisplay import Display 
#display = Display(visible=0, size=(1024, 768)) 
#display.start() 
driver = webdriver.Chrome("chromedriver", options=chrome_options)
screenshot_name = "screenshot.png"
chat_id = "-1001620964109"


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def check(update: Update, context: CallbackContext) -> None:
    result = check_site()

    with open(screenshot_name, 'rb') as f:
        update.message.reply_photo(photo=f, timeout=50)

    update.message.reply_text(result['body'])

def check_site():
    error = False
    result = "=====\n"
    try:
        """Echo the user message."""
        #data_row = '------WebKitFormBoundarygVxB5IACyQXle244\r\nContent-Disposition: form-data; name="email"\r\n\r\nchdima@gmail.com\r\n------WebKitFormBoundarygVxB5IACyQXle244\r\nContent-Disposition: form-data; name="password"\r\n\r\nAa050658655\r\n------WebKitFormBoundarygVxB5IACyQXle244\r\nContent-Disposition: form-data; name="token_name"\r\n\r\n1\r\n------WebKitFormBoundarygVxB5IACyQXle244\r\nContent-Disposition: form-data; name="os_type"\r\n\r\nweb\r\n------WebKitFormBoundarygVxB5IACyQXle244--\r\n'
        #data = {"email": "chdima@gmail.com", "password": "nAa050658655"}
        #headers1 = {
        #    'Accept': 'application/json',
        #}
        #headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}

        #files = dict(email='chdima@gmail.com', password='Aa050658655', token_name='1', os_type='web')
        #url = "https://app-v2.growdirector.com/api/v1/sessions"
        #response = requests.get(url, files=files, headers=headers) #json=data)
        #print("===============ilshat")
        #if (response.status_code == 200):
        #    print(response.json())
        #    update.message.reply_text('login 200: ' + response.text)
        #else:
        #    update.message.reply_text('Cannot login: code = ' + response.status_code)
        driver.get("https://app-v2.growdirector.com/login")
        result += "try to login: https://app-v2.growdirector.com/login \n"


        driver.find_element(by=By.CSS_SELECTOR, value="input[class='login-input-item'][type='email']").send_keys("chdima@gmail.com")
        password = driver.find_element(by=By.CSS_SELECTOR, value="input[class='login-input-item'][type='password']")
        password.send_keys("Aa050658655")
        password.send_keys(Keys.RETURN)

        result += "submit login \n"

        time.sleep(10)
        driver.save_screenshot(screenshot_name)

        result += "save screenshot \n"

        sensors_items = driver.find_elements(by=By.CLASS_NAME, value="dashboard-sensors-item")
        sockets_items = driver.find_elements(by=By.CLASS_NAME, value="dashboard-sockets-item")

        result += 'sensors items count ' + str(len(sensors_items)) + '\n'
        result += 'ssockets items count ' + str(len(sockets_items)) + '\n'

        driver.find_element(by=By.CLASS_NAME, value="header-logout-btn").click()
        result += "logout \n"
    except:
        error = True
        result += "Something wrong!!! \n"

    return dict({"error": error, "body": result})


def echo(update: Update, context: CallbackContext) -> None:
    result = check_site()

    with open(screenshot_name, 'rb') as f:
        update.message.reply_photo(photo=f, timeout=50)

    update.message.reply_text(result['body'])


def callback_hour(context: CallbackContext):
    result = check_site()

    now_utc = datetime.now(timezone.utc) # 7 utc = 10 msk
    if now_utc.hour == 7 or result['error']:
        context.bot.send_message(chat_id=chat_id, text=result['body'])
        with open(screenshot_name, 'rb') as f:
            context.bot.send_photo(chat_id=chat_id, photo=f, timeout=50)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("", use_context=True)
    job = updater.job_queue

    #job.run_once(callback, 1)
    interval = 60 * 60 # hour
    job.run_repeating(callback_hour, interval=interval, first=10)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("check", check))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
