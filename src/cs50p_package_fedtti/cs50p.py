import os
from dotenv import load_dotenv
import discord
import re
from openai import OpenAI

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello') or message.content.startswith('hi'):
        await message.channel.send('hello, world')

    if client.user.mentioned_in(message):
        msg = ''

        if re.search('thank', message.content):
            msg = 'you\'re welcome, {}'.format(message.author.mention)

        else:
            msg = 'got it, {}'.format(message.author.mention)

        await message.channel.send(msg)

    if not message.guild:
        # TODO: @fedtti - Start a conversation using GTP-4o.
        await message.channel.send('got it')
        return


client.run(DISCORD_TOKEN)
