import asyncio
import json
from os.path import exists

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

    def __init__(self, notification_service: NotificationService):
        self.__client = TgtgClient(email=TGTG_EMAIL)
        self._notification_service = notification_service

    async def launch(self):
        while self.__is_running:
            # refresh credentials
            self.__credentials = Credentials(**self.__client.get_credentials())

            favorites = [Favorite(v['display_name'], v['items_available'], v['in_sales_window'])
                         for v in self.__client.get_items()]

            [self._notification_service.notify(message=repr(favorite))
             for favorite in filter(lambda f: f.is_available, favorites)]

            await asyncio.sleep(WATCHER_FREQUENCY)

    async def connect(self):
        if exists("./credentials.json"):
            with open("./credentials.json", "r") as file:
                tmp = json.loads(file.read())
                self.__credentials = Credentials(**tmp)
        else:
            tmp = self.__client.get_credentials()
            self.__credentials = Credentials(**tmp)
            with open("./credentials.json") as file:
                file.write(json.dumps(self.__credentials))

    def stop(self):
        self.__is_running = False
