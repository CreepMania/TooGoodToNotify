import telegram_send

from src.environment import TELEGRAM_CONFIG_PATH
from src.notifications.notification_service import NotificationService, MessageType


class TelegramNotificationService(NotificationService):
    def __init__(self):
        pass

    def notify(self, message: str, title: str = "", message_type: MessageType = MessageType.INFO):
        telegram_send.send(conf=TELEGRAM_CONFIG_PATH, messages=[message])
