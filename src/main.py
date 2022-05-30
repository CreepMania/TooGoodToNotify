import asyncio
import logging
import sys
from http import HTTPStatus

from src.environment import WATCHER_FREQUENCY, LOG_LEVEL
from src.notifications import TelegramNotificationService, MessageType
from src.tgtg import TgtgAPIError
from src.watcher import Watcher

logger = logging.getLogger(__name__)


def init_logger():
    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL,
                        format='%(asctime)-2s | %(levelname)-5s - %(name)-10s -  %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S")


async def main():
    notifier = TelegramNotificationService()
    notifier.notify(title="🏁 Start", message="Process has started successfully 🎉")
    try:
        watcher: Watcher = Watcher(notifier)
        await watcher.connect()
        await watcher.launch()
    except TgtgAPIError as ex:
        logger.error(ex)
        status_code, msg = ex.args
        if status_code == HTTPStatus.TOO_MANY_REQUESTS:
            notifier.notify(title=msg, message=repr(ex), message_type=MessageType.ERROR)
            await asyncio.sleep(30 * 60)  # sleep 30 minutes
        else:
            notifier.notify(title=msg, message=repr(ex), message_type=MessageType.ERROR)
            await asyncio.sleep(WATCHER_FREQUENCY)
    except Exception as ex:
        logger.error(ex)
        notifier.notify(title=str(ex), message=repr(ex), message_type=MessageType.ERROR)
        await asyncio.sleep(WATCHER_FREQUENCY)


if __name__ == "__main__":
    init_logger()
    asyncio.run(main())
