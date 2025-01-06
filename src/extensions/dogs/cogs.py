import discord
from discord import app_commands
from discord.ext import commands
import requests
from io import BytesIO
import random
import re
from bs4 import BeautifulSoup
from discord.ui import Button, View
import time

def getRandomSticker(url: str, min_length: int = 3, max_length: int = 7) -> str:
    try:
        # Отправляем GET-запрос
        response = requests.get(url)
        response.raise_for_status()

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        emojis_section = soup.find_all('div', class_='emojis')

        if emojis_section:
            emojis = []
            for emoji_block in emojis_section:
                emojis.extend(emoji_block.get_text().strip().splitlines())

            # Фильтруем всо
            
            filtered_emojis = [
                emoji for emoji in emojis
                if re.match(r'^[^🐶🐕🐩🐾🎐⭐️🫧🌀👦🍫🎩🍦🌊🖤🍪👀👧👅👽👻🤡✨]+$', emoji)
                and min_length < len(emoji.strip()) < max_length
            ]

            if filtered_emojis:
                random_emoji = random.choice(filtered_emojis)
                return f"{random_emoji}"

            print(f"Нет подходящих текстовых эмодзи, длина которых от {min_length} до {max_length} символов.")
            return "(｡♥‿♥｡)"

        print(f"Не удалось найти эмодзи на странице.")
        return "(｡♥‿♥｡)"
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return "(｡♥‿♥｡)"

# Кнопка для при нажатии на которую будет отправляться новая собачка


import discord
import requests
import time
from discord.ui import Button, View
from io import BytesIO

class AnotherDogButton(Button):
    def __init__(self):
        super().__init__(label="Another 🐶", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        # Замер времени для запроса изображения
        startTime = time.time()
        dogImageResponse = requests.get("https://dog.ceo/api/breeds/image/random")
        dogImageData = dogImageResponse.json()
        dogImageUrl = dogImageData["message"]
        imageRequestTime = (time.time() - startTime) * 1000

        # Замер времени для запроса факта
        startTime = time.time()
        dogFactResponse = requests.get("https://dog-api.kinduff.com/api/facts")
        dogFactData = dogFactResponse.json()
        dogFact = dogFactData["facts"][0]
        factRequestTime = (time.time() - startTime) * 1000
        
        # Получаем изображение
        startTime = time.time()
        dogImage = requests.get(dogImageUrl).content
        imageRequestTimeTotal = (time.time() - startTime) * 1000
        imageFile = discord.File(BytesIO(dogImage), filename="dogImage.jpg")

        cuteSticker = getRandomSticker("https://emojicombos.com/cute")
        maxRequestTime = max(imageRequestTime, factRequestTime, imageRequestTimeTotal)

        # Создаем Embed
        embed = discord.Embed(
            title=f"{cuteSticker}",
            description=f"**Dog Fact:** {dogFact}",
            color=0xFFFFFF
        )
        embed.set_image(url="attachment://dogImage.jpg")
        embed.set_footer(text=f"**request took: {maxRequestTime:.2f}ms**")

        view = View()
        view.add_item(AnotherDogButton())
        await interaction.response.send_message(embed=embed, file=imageFile, view=view)

class DogCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="dog", description="Рандомная картинка собаки и факт о ней")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def dog(self, interaction: discord.Interaction):
        await interaction.response.defer()

        startTime = time.time()
        dogImageResponse = requests.get("https://dog.ceo/api/breeds/image/random")
        dogImageData = dogImageResponse.json()
        dogImageUrl = dogImageData["message"]
        imageRequestTime = (time.time() - startTime) * 1000

        # Замер времени для запроса факта
        startTime = time.time()
        dogFactResponse = requests.get("https://dog-api.kinduff.com/api/facts")
        dogFactData = dogFactResponse.json()
        dogFact = dogFactData["facts"][0]
        factRequestTime = (time.time() - startTime) * 1000

        # Получаем изображение
        startTime = time.time()
        dogImage = requests.get(dogImageUrl).content
        imageRequestTimeTotal = (time.time() - startTime) * 1000
        imageFile = discord.File(BytesIO(dogImage), filename="dogImage.jpg")

        # Получаем случайный текстовый стикер с сайта
        cuteSticker = getRandomSticker("https://emojicombos.com/cute")
        
        maxRequestTime = max(imageRequestTime, factRequestTime, imageRequestTimeTotal)

        embed = discord.Embed(
            title=f"{cuteSticker}",
            description=f"**Dog Fact:** {dogFact}",
            color=0xFFFFFF
        )
        embed.set_image(url="attachment://dogImage.jpg")
        embed.set_footer(text=f"Max request time: {maxRequestTime:.2f}ms")

        view = View()
        view.add_item(AnotherDogButton())

        await interaction.followup.send(embed=embed, file=imageFile, view=view)