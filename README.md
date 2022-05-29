# TooGoodToNotify

Simple project that aims to notify a user that a favorite bag is available

Tested on Python 3.9 and 3.10, incompatible with Python <= 3.7

## Setup

Run `pip install -r requirements.txt` to install all dependencies. \
Then create a bot on Telegram using [BotFather](https://telegram.me/BotFather) and
use `telegram-send --configure --config telegram-send.conf` to configure the `telegram-send` library. \
Define the `TGTG_EMAIL` environment variable and/or the others defined in the `example.env` file

Finally, run with `python main.py`
to start the process, and you should receive a notification by the Telegram bot you created

## TODO:

☑️ Watch a user bags using tgtg package \
☑️ Notify once a bag is available \
☑️ Implement Telegram notifications \
☑️ Notify errors \
☑️ Notify when TooGoodToGo requires connection verification \
☑️ Logs !!! \
☑️ Better notification formatting
