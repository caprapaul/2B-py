import discord
from discord.ext import commands
import asyncio
import config
import os


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            description=config.description,
            command_prefix=config.prefix
        )

        for name in os.listdir(config.cog_dir):
            if name.startswith('__'):
                continue

            self.load_extension(f'{config.cog_dir}.{name}')

    def run(self):
        super().run(config.token, reconnect=True)

    async def on_ready(self):
        print(f"Username: {self.user}\nID: {self.user.id}")