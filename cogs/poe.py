import discord
import requests
from discord.ext import commands


class Poe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Poe is ready')

    @commands.command(aliases=['poeUnique'])
    async def poe_unique(self, ctx, *, item_name):
        print(item_name)
        poe_wiki_api = 'https://pathofexile.gamepedia.com/api.php?action=cargoquery&tables=items&fields=name'\
                       f'&where=rarity="Unique" AND name LIKE "%{item_name}%"&group_by=name&format=json'
        await ctx.message.add_reaction('❗')
        r = requests.get(poe_wiki_api)
        print(r.content)
        await ctx.message.remove_reaction('❗', self.client.user)
        await ctx.message.add_reaction('✔')


def setup(client):
    client.add_cog(Poe(client))
