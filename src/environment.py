import logging
import os
from zoneinfo import ZoneInfo

TGTG_EMAIL = os.getenv("TGTG_EMAIL")
WATCHER_FREQUENCY = int(os.getenv("WATCHER_FREQUENCY", default=60))
TELEGRAM_CONFIG_PATH = os.getenv("TELEGRAM_CONFIG_PATH", default="../telegram-send.conf")
LOG_LEVEL = int(os.getenv("LOG_LEVEL", default=logging.INFO))
CACHE_CREDENTIALS = bool(os.getenv("CACHE_CREDENTIALS", default=True))
TZ_INFO = ZoneInfo(os.getenv("TZ_INFO", default="UTC"))
