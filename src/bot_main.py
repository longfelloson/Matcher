import asyncio

from bot.notifications.consumer import read_notifications
from bot.notifications.new_users.consumer import read_new_users
from bot.utils import start_bot


async def main():
    await asyncio.gather(
        read_new_users(),
        read_notifications(),
        start_bot()
    )


if __name__ == "__main__":
    asyncio.run(main())
