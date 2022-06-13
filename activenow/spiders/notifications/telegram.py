import os

from telethon import TelegramClient, sync

from .base import BaseNotificationBackend


class TelegramBackend(BaseNotificationBackend):
    def run(self):
        api_id = os.getenv("TELEGRAM_API_ID", 0)
        api_hash = os.getenv("TELEGRAM_API_HASH", 0)
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        group_id = int(os.getenv("TELEGRAM_GROUP_ID"))

        bot_client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
        # connecting and building the session
        bot_client.connect()
        try:
            bot_client.send_message(group_id, self.message, parse_mode="html")
        except Exception as e:
            # there may be many error coming in while like peer
            # error, wrong access_hash, flood_error, etc
            print(e)
        # disconnecting the telegram session
        # client.disconnect()
        bot_client.disconnect()
