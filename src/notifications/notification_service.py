from abc import ABCMeta, abstractmethod
from enum import Enum


class MessageType(Enum):
    INFO = 1,
    ERROR = 2


class NotificationService(metaclass=ABCMeta):
    @abstractmethod
    def notify(self, message: str, title: str = "", message_type: MessageType = MessageType.INFO):
        pass
