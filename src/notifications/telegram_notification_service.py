from datetime import datetime, timedelta

import telegram_send

from src.environment import TELEGRAM_CONFIG_PATH
from src.models import Favorite
from src.notifications.notification_service import NotificationService, MessageType


class TelegramNotificationService(NotificationService):
    __template = "<b>{0}{1}</b>\n\n{2}"

    def __init__(self):
        super().__init__()

    def notify(self, message: str, title: str, message_type: MessageType = MessageType.INFO):
        # don't send if message is identical and less than and hour old
        if self._last_message == message and self._last_message_date >= datetime.today() - timedelta(hours=1):
            return

        self._last_message = message
        self._last_message_date = datetime.today()

        msg = self.__template.format(f"[{message_type.name}] " if message_type != MessageType.INFO else "",
                                     title,
                                     message)

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[msg], parse_mode="html", disable_web_page_preview=True)

    def notify_favorite(self, item: Favorite):
        title = f"{item.display_name}"
        message = f"{item.items_available} items are available !\nhttps://share.toogoodtogo.com/item/{item.item_id}/"

        msg = self.__template.format("",
                                     title,
                                     message)

        # don't send if message is identical and less than and hour old
        if self._last_message == message and self._last_message_date >= datetime.today() - timedelta(hours=1):
            return

        self._last_message = message
        self._last_message_date = datetime.today()

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[msg], parse_mode="html", disable_web_page_preview=True)

