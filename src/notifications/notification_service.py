from datetime import datetime
from abc import ABCMeta, abstractmethod
from enum import Enum

from src.models import Favorite


class MessageType(Enum):
    INFO = 1,
    WARNING = 2,
    ERROR = 3


class NotificationService(metaclass=ABCMeta):
    _last_message: str
    _last_message_date: datetime

    def __init__(self):
        self._last_message = None
        self._last_message_date = None

    @abstractmethod
    def notify(self, message: str, title: str, message_type: MessageType = MessageType.INFO):
        pass

    @abstractmethod
    def notify_favorite(self, item: Favorite):
        pass
