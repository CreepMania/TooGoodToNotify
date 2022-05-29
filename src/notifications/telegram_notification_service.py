from datetime import datetime, timedelta

import telegram_send

from src.environment import TELEGRAM_CONFIG_PATH, TZ_INFO
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

        msg = self.__template.format(f"{message_type.emoji} "
                                     if message_type != MessageType.INFO else "",
                                     title,
                                     message)

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[msg], parse_mode="html", disable_web_page_preview=True)

    def notify_available(self, item: Favorite):
        title = f"🥘 {item.display_name}"
        message = f"⏳ <b>{item.pickup_interval.start.astimezone(TZ_INFO):%Y-%m-%d %H:%M}</b>\n" \
                  f"⌛ <b>{item.pickup_interval.end.astimezone(TZ_INFO):%Y-%m-%d %H:%M}</b>\n\n" \
                  f"{item.items_available} baskets are available!\n" \
                  f"https://share.toogoodtogo.com/item/{item.item_id}/"

        msg = self.__template.format("",
                                     title,
                                     message)

        # don't send if message is identical and less than and hour old
        if self._last_message == message and self._last_message_date >= datetime.today() - timedelta(hours=1):
            return

        self._last_message = message
        self._last_message_date = datetime.today()

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[msg], parse_mode="html", disable_web_page_preview=True)
