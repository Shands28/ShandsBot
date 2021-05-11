import random
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='!')
statuses = ['Stat1', 'Stat2', 'Stat3']


@client.event
async def on_ready():
    print('Logged on as', client.user)
    await client.change_presence(activity=discord.Game(name='Pinturillo 3: El desenlace'), status=discord.Status.dnd)


@client.command()
async def load(ctx, extension):
    if ctx.message.author == 'Shands#6980':
        client.load_extension(f'cogs.{extension}')
    else:
        return


@client.command()
async def unload(ctx, extension):
    if ctx.message.author == 'Shands#6980':
        client.unload_extension(f'cogs.{extension}')
    else:
        return


@client.command()
async def ping(message):
    if message.author == client.user:
        return
    await message.send('pong')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Yes', 'No', 'Try Again']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    async for message in channel.history(limit=int(amount)):
        await message.delete()


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


# async def change_status():
#     await client.wait_until_ready()
#     msgs = cycle(statuses)
#
#     while not client.is_closed:
#         current_status = next(msgs)
#         print(current_status)
#         await client.change_presence(activity=discord.Game(name=current_status))
#         await asyncio.sleep(1)

# client.loop.create_task(change_status())

token = open('token', 'r')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token.read())
