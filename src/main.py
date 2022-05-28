import asyncio

from src.notifications import TelegramNotificationService
from src.watcher import Watcher


async def main():
    notifier = TelegramNotificationService()
    watcher: Watcher = Watcher(notifier)
    await watcher.connect()
    await watcher.launch()


if __name__ == "__main__":
    asyncio.run(main())
