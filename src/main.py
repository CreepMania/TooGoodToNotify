import asyncio
from http import HTTPStatus

from tgtg import TgtgAPIError

from src.notifications import TelegramNotificationService, MessageType
from src.watcher import Watcher


async def main():
    notifier = TelegramNotificationService()
    try:
        watcher: Watcher = Watcher(notifier)
        await watcher.connect()
        await watcher.launch()
    except TgtgAPIError as ex:
        status_code, msg = ex
        if status_code == HTTPStatus.TOO_MANY_REQUESTS:
            notifier.notify(message=msg, message_type=MessageType.ERROR)
            await asyncio.sleep(30 * 60)  # sleep 30 minutes
        else:
            notifier.notify(message=repr(ex), message_type=MessageType.ERROR)
    except Exception as ex:
        notifier.notify(message=repr(ex), message_type=MessageType.ERROR)


if __name__ == "__main__":
    asyncio.run(main())
