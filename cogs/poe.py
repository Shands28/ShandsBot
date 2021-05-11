import json
import ssl
import discord
import pymongo
from discord.ext import commands

with open("credentials.json") as file:
    credentials = json.load(file)
client = pymongo.MongoClient(
    f"mongodb+srv://{credentials['user']}:{credentials['pass']}@cluster0.tejv0.mongodb.net"
    "/PoE?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client.PoE


class Poe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Poe is ready')

    @commands.command(aliases=['poeunique'])
    async def poe_unique(self, ctx, *, item_name):
        print(item_name)
        await ctx.message.add_reaction('🔄')
        result = db.Uniques.find({"name": {"$regex": item_name, "$options": 'i'}})
        for x in result:
            print(x)
        embed = discord.Embed(
            title=f"{result.count()} unique{'s' if result.count() > 1 else ''} found",
            description='',
            colour=discord.Colour.blurple()
        )
        embed.set_thumbnail(url='https://gamepedia.cursecdn.com/pathofexile_gamepedia/thumb/1/12/Path_of_Exile_logo.png'
                                '/300px-Path_of_Exile_logo.png?version=22e4fb4a0345ac18d6b6cdafb9cc335a')
        await ctx.message.remove_reaction('🔄', self.client.user)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Poe(client))
