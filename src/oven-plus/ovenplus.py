# Oven+ - 2025 Freakybob Team (under Unlicense)
# Oven+ lets you generate images using Google Gemini.
# Credits:
# Names - Creator of Oven+ and developer
# Nomaakip - Developer
# Wish - Original creator of Oven
# Hypercuber - Made the icon
# ChatGPT - Debugger
from google import genai # pip install -q -U google-genai
from google.genai import types
import discord # pip install -U discord.py
import requests
from io import BytesIO
from google.api_core.exceptions import ResourceExhausted # pip install google-api-core

client = genai.Client(api_key="your gemini api key") # get key https://aistudio.google.com/app/apikey

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if str(self.user.id) in message.content:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=message.content,
                    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
                )
                candidate = response.candidates[0].content

                for part in candidate.parts:
                    if part.text:
                        await message.channel.send(part.text)
                    elif getattr(part, 'inline_data', None):
                        img_bytes = part.inline_data.data
                        await message.channel.send(
                            file=discord.File(BytesIO(img_bytes), filename="oven_image.png")
                        )
            except ResourceExhausted:
                await message.channel.send("The oven is exhausted. Please wait up to 24 hours for your key to reset. (429: RESOURCE_EXHAUSTED)")
            except Exception as e:
                await message.channel.send(f"Error: {str(e)}")

        if "oven, shutdown" in message.content:
            await message.channel.send("BOT: Oven is going down for updates... thank you :D")

intents = discord.Intents.default()
intents.message_content = True
discord_client = MyClient(intents=intents)
discord_client.run("your discord bot token") # get token https://discord.com/developers/applications