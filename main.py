import discord
from discord.ext import commands
import asyncio
from itertools import cycle

client = commands.Bot(command_prefix='!')
statuses = ['Stat1', 'Stat2', 'Stat3']


@client.event
async def on_ready():
    print('Logged on as', client.user)
    await client.change_presence(activity=discord.Game(name='Pinturillo 3: El desenlace'))


@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return

    if message.content[1:] == 'ping':
        await message.channel.send('pong')


@client.event
async def on_reaction_add(reaction, user):
    print(reaction)
    print(user)
    if reaction.message.author != client.user:
        await reaction.message.add_reaction(reaction)
    return


@client.event
async def on_reaction_remove(reaction, user):
    print(reaction)
    print(user)
    if reaction.message.author != client.user:
        await reaction.message.remove_reaction(reaction, client.user)
    return


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(statuses)

    while not client.is_closed:
        current_status = next(msgs)
        print(current_status)
        await client.change_presence(activity=discord.Game(name=current_status))
        await asyncio.sleep(1)


token = open('token.txt', 'r')
client.loop.create_task(change_status())
client.run(token.read())
