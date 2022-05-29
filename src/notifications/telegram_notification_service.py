from datetime import datetime, timedelta

import telegram_send

from src.environment import TELEGRAM_CONFIG_PATH
from src.notifications.notification_service import NotificationService, MessageType


class TelegramNotificationService(NotificationService):
    def __init__(self):
        super().__init__()

    def notify(self, message: str, title: str = "", message_type: MessageType = MessageType.INFO):
        # don't send if message is identical and less than and hour old
        if self._last_message == message and self._last_message_date >= datetime.today() - timedelta(hours=1):
            return

        self._last_message = message
        self._last_message_date = datetime.today()

        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[message])
