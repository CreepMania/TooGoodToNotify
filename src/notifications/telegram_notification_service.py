import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from logging import Logger
from typing import List

import telegram_send

from src.environment import TELEGRAM_CONFIG_PATH, TZ_INFO
from src.models import Favorite
from src.notifications.notification_service import NotificationService, MessageType


@dataclass
class TelegramNotification:
    message: str
    send_date: datetime

    def __init__(self, message: str):
        self.message = message
        self.send_date = datetime.today()

    @property
    def is_cache_expired(self):
        return self.send_date + timedelta(hours=1) < datetime.today()


class TelegramNotificationService(NotificationService):
    __template = "<b>{0}{1}</b>\n\n{2}"
    _last_messages: List[TelegramNotification]
    __logger: Logger

    def __init__(self):
        super().__init__()
        self._last_messages = []
        self.__logger = logging.getLogger(__name__)

    def notify(self, message: str, title: str, message_type: MessageType = MessageType.INFO):
        # don't send if message is identical

        notification = list(filter(lambda m: m.message == message, self._last_messages))
        if len(notification) > 0:
            return

        self._last_messages.append(TelegramNotification(message))

        msg = self.__template.format(f"{message_type.emoji} "
                                     if message_type != MessageType.INFO else "",
                                     title,
                                     message)

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[msg], parse_mode="html", disable_web_page_preview=True)
        self.__clean_cache()

    def notify_available(self, item: Favorite):
        title = f"🥘 {item.display_name}"
        day = "Today" if item.pickup_interval.start.day == datetime.today().day else "Tomorrow"
        message = f"⏳ {day} ({item.pickup_interval.start:%d/%m}) " \
                  f"<b>from {item.pickup_interval.start.astimezone(TZ_INFO):%H:%M}</b>\n" \
                  f"⌛ until <b>{item.pickup_interval.end.astimezone(TZ_INFO):%H:%M}</b>\n\n" \
                  f"{item.items_available} baskets are available!\n" \
                  f"https://share.toogoodtogo.com/item/{item.item_id}/"

        msg = self.__template.format("",
                                     title,
                                     message)

        # don't send if message is identical
        notification = list(filter(lambda m: m.message == message, self._last_messages))
        if len(notification) > 0:
            return

        self._last_messages.append(TelegramNotification(message))

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[msg], parse_mode="html", disable_web_page_preview=True)
        self.__clean_cache()

    def __clean_cache(self):
        last_messages = [m for m in self._last_messages if not m.is_cache_expired]
        if len(self._last_messages) - len(last_messages) > 0:
            self.__logger.debug(f"Cleaned {len(self._last_messages) - len(last_messages)} notifications from cache")
            self._last_messages = last_messages
