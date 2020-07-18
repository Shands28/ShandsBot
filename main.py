import random
import requests
import discord
from discord.ext import commands
import asyncio
from itertools import cycle

client = commands.Bot(command_prefix='!')
statuses = ['Stat1', 'Stat2', 'Stat3']


@client.event
async def on_ready():
    print('Logged on as', client.user)
    await client.change_presence(activity=discord.Game(name='Pinturillo 3: El desenlace'), status=discord.Status.dnd)


@client.command()
async def ping(message):
    if message.author == client.user:
        return
    await message.send('pong')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Yes', 'No', 'Try Again']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(aliases=['poeUnique'])
async def poe_unique(ctx, *, item_name):
    print(item_name)
    poe_wiki_api = 'https://pathofexile.gamepedia.com/api.php?action=cargoquery&tables=items&fields=name&where=rarity' \
                   f'="Unique" AND name LIKE "%{item_name}%"&group_by=name&format=json'
    await ctx.message.add_reaction('❗')
    r = requests.get(poe_wiki_api)
    print(r.content)
    await ctx.message.remove_reaction('❗', client.user)


@client.event
async def on_reaction_add(reaction, user):
    print(reaction)
    print(user)
    if user != client.user:
        await reaction.message.add_reaction(reaction)
    return


@client.event
async def on_reaction_remove(reaction, user):
    print(reaction)
    print(user)
    if user != client.user:
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
