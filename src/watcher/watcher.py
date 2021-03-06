import asyncio
import dataclasses
import datetime
import json
import logging
import os.path
from json import JSONDecodeError
from logging import Logger
from typing import Tuple

from src.models import Credentials
from src.models import Favorite, PickupInterval
from src.notifications import NotificationService
from src.tgtg import TgtgClient
from ..environment import TGTG_EMAIL, WATCHER_FREQUENCY, CACHE_CREDENTIALS, TZ_INFO

CREDENTIAL_PATH = "./credentials.json"


class Watcher:
    _notification_service: NotificationService
    __client: TgtgClient = None
    __credentials: Credentials = None
    __is_running: bool = True
    __activity_period: Tuple[int, int] = (8, 23)  # active between 8 am and 11 pm

    __logger: Logger

    def __init__(self, notification_service: NotificationService):
        self.__logger = logging.getLogger(__name__)
        self._notification_service = notification_service

    async def connect(self) -> None:
        """
        Tries to connect to the TooGoodToGo API
        Uses cached credentials if they exist
        """
        if CACHE_CREDENTIALS and os.path.exists(CREDENTIAL_PATH) and os.path.getsize(CREDENTIAL_PATH) > 0:
            self.__logger.debug("Reusing credentials stored in 'credentials.json' file")
            with open(CREDENTIAL_PATH, "r") as file:
                file_content = file.read()
                if len(file_content) > 0:
                    try:
                        tmp = json.loads(file_content)
                        self.__credentials = Credentials(**tmp)
                    except (JSONDecodeError, TypeError) as ex:
                        self.__logger.warning(ex)

        if self.__credentials is None or not self.__credentials.is_valid:
            self.__client = TgtgClient(email=TGTG_EMAIL,
                                       notification_service=self._notification_service
                                       )
            self.__credentials = Credentials(**self.__client.get_credentials())

        if CACHE_CREDENTIALS:
            with open(CREDENTIAL_PATH, 'w') as file:
                file.write(json.dumps(dataclasses.asdict(self.__credentials)))

        self.__client = TgtgClient(email=TGTG_EMAIL,
                                   access_token=self.__credentials.access_token,
                                   refresh_token=self.__credentials.refresh_token,
                                   user_id=self.__credentials.user_id,
                                   notification_service=self._notification_service
                                   )

    async def launch(self):
        start, end = self.__activity_period
        self.__logger.info("Started")
        while self.__is_running:
            current_hour = datetime.datetime.today().astimezone(TZ_INFO).hour
            if not (start <= current_hour < end):
                await asyncio.sleep(WATCHER_FREQUENCY)

            # refresh credentials
            self.__credentials = Credentials(**self.__client.get_credentials())
            favorites = [Favorite(v['display_name'],
                                  v['items_available'],
                                  v['in_sales_window'],
                                  v['item']['item_id'],
                                  PickupInterval(**v.get('pickup_interval') or {}))
                         for v in self.__client.get_items()]
            self.__logger.info(f"Found {len(favorites)} favorites")

            # filter on available
            favorites = list(filter(lambda favorite: favorite.is_available, favorites))
            self.__logger.info(f"Found {len(favorites)} available favorites!")

            [self._notification_service.notify_available(favorite) for favorite in favorites]

            self.__logger.debug("Sleeping...")
            await asyncio.sleep(WATCHER_FREQUENCY)

    def stop(self):
        self.__logger.info("Stopping...")
        self.__is_running = False
