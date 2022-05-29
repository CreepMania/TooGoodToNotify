import asyncio
import json
import logging
from logging import Logger
from os.path import exists
from typing import List

from tgtg import TgtgClient
from ..environment import TGTG_EMAIL, WATCHER_FREQUENCY
from src.models import Credentials
from src.models import Favorite
from src.notifications import NotificationService


class Watcher:
    _notification_service: NotificationService
    __client: TgtgClient
    __credentials: Credentials
    __is_running: bool = True

    __favorite_cache: List[Favorite] = None
    __logger: Logger

    def __init__(self, notification_service: NotificationService):
        self.__logger = logging.getLogger(__name__)
        self._notification_service = notification_service

    async def launch(self):
        self.__logger.info("Started")
        while self.__is_running:
            # refresh credentials
            self.__credentials = Credentials(**self.__client.get_credentials())

            favorites = [Favorite(v['display_name'], v['items_available'], v['in_sales_window'])
                         for v in self.__client.get_items()]
            self.__logger.info(f"Found {len(favorites)} favorites")
            # filter on new alerts only, or if Favorite is expired
            if self.__favorite_cache is not None:
                favorites = [f for f in favorites if f not in self.__favorite_cache or f.is_expired]

            # filter on available
            favorites = [favorite for favorite in favorites if favorite.is_available]
            self.__logger.info(f"Found {len(favorites)} available favorites!")

            [self._notification_service.notify(message=repr(favorite)) for favorite in favorites]

            self.__favorite_cache = favorites

            self.__logger.debug("Sleeping...")
            await asyncio.sleep(WATCHER_FREQUENCY)

    async def connect(self):
        if exists("./credentials.json"):
            self.__logger.debug("Reusing credentials stored in 'credentials.json' file")
            with open("./credentials.json", "r") as file:
                tmp = json.loads(file.read())
                self.__credentials = Credentials(**tmp)
        else:
            self.__logger.debug("Connecting to TooGoodToGo API...")
            tmp = self.__client.get_credentials()
            self.__credentials = Credentials(**tmp)
            with open("./credentials.json") as file:
                file.write(json.dumps(self.__credentials))

        self.__client = TgtgClient(email=TGTG_EMAIL,
                                   access_token=self.__credentials.access_token,
                                   refresh_token=self.__credentials.refresh_token,
                                   user_id=self.__credentials.user_id,
                                   notification_service=self._notification_service
                                   )

    def stop(self):
        self.__logger.info("Stopping...")
        self.__is_running = False
