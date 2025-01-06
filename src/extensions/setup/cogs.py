import discord
from discord.ext import commands
from discord.gateway import DiscordWebSocket
import sys
from colorama import Fore, Style, init
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(env_path)
token = os.getenv('TOKEN')

bannerUrl = "https://i.postimg.cc/sxZH9bzH/banner.png"

class MobileModeWebSocket(DiscordWebSocket):
    """
    Кастомный WebSocket-клиент, который имитирует Discord Android
    """
    async def identify(self):
        payload = {
            'op': self.IDENTIFY,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'Discord Android',
                    '$device': 'Discord Android',
                    '$referrer': '',
                    '$referring_domain': ''
                },
                'compress': True,
                'large_threshold': 250,
                'v': 3
            }
        }

        if self.shard_id is not None and self.shard_count is not None:
            payload['d']['shard'] = [self.shard_id, self.shard_count]

        state = self._connection

        payload['d']['presence'] = {
            'status': "idle",
            'activities': [
                {
                    'name': "Developer: Deleted User (401)",
                    'type': 3,
                }
            ],
            'since': 0,
            'afk': True
        }

        if state._intents is not None:
            payload['d']['intents'] = state._intents.value

        await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
        await self.send_as_json(payload)


class mobileAFKModeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.override_websocket()

    def override_websocket(self):
        DiscordWebSocket.identify = MobileModeWebSocket.identify
        print(f"{Fore.BLUE}WebSocket клиента изменён для мобильного режима.")
        
class BotInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def setBotSettings(self):
        if self.bot.user is None:
            return

        # Устанавливаем имя бота
        await self.bot.user.edit(username="Dog Bot")

        # Устанавливаем аватарку
        avatar_url = "https://i.postimg.cc/L8Z4g8Gj/avatar.jpg"
        avatar_image = requests.get(avatar_url).content
        avatar_file = BytesIO(avatar_image)
        await self.bot.user.edit(avatar=avatar_file.read())

        # Устанавливаем баннер
        
        # --
        

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setBotSettings()