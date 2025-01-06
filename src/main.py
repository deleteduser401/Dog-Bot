# Основной файл бота

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from colorama import Fore, Style, init
import asyncio

init(autoreset=True)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(
    command_prefix="!",
    intents=intents,
)

@client.event
async def on_ready():
    await client.tree.sync()
    if client.user is None:
        print(f"{Fore.RED}client.user is None!{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}Bot Name: {Fore.YELLOW}{client.user.name}")
    print(f"{Fore.CYAN}Bot ID: {Fore.YELLOW}{client.user.id}")
    print(f"{Fore.CYAN}Status: {Fore.GREEN}Online")
    print(f"{Fore.CYAN}Created: {Fore.YELLOW}by Deleted User (401)")
    print(f"{Fore.GREEN}#=================================")


async def load_extensions() -> None:
    try:
        await client.load_extension("extensions.setup.setup")
        await client.load_extension("extensions.dogs.setup")
        print(f"{Fore.GREEN}Successfully loaded {Fore.YELLOW}'setup' {Fore.GREEN}extension.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to load 'setup' extension: {e}{Style.RESET_ALL}")


async def main():
    print(f"{Fore.BLUE}#========== INITIALIZING BOT =========={Style.RESET_ALL}")
    await load_extensions()

    token = os.getenv("TOKEN")
    if token:
        print(f"{Fore.BLUE}Starting the bot...{Style.RESET_ALL}")
        await client.start(token)
    else:
        print(f"{Fore.RED}Token not found. Please set the TOKEN environment variable.{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())