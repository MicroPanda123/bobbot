import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import os
from dotenv import load_dotenv
import openai

load_dotenv()
#
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_prompt = "You are Bob, you are a discord bot made to entertain people on this server. Be funny, but also little cranky if needed.\nHuman: "
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(activity=discord.Game("being bob"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  if client.user.mentioned_in(message):
    print("Requesting response.")
    print(msg)
    response = openai.Completion.create(
      engine="text-davinci-001",
      prompt=openai_prompt + msg.replace("<@!772573761941274654>", "", 1) + "\nAi:",
      max_tokens=64,
      stop="Human:"
    )
    response = response['choices'][0]['text'].strip()
    await message.channel.send(response)
    
client.run(os.getenv("DISCORD_TOKEN"))

