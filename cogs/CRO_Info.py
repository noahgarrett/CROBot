import discord
from discord.ext import commands, tasks
import json
import main

class CROInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="price", help='!price | Retrieve the current price for CRO')
    async def price(self, ctx):
        data = main.get_coin("CRO")
        price = data['price']
        await ctx.send(f'${price}')

def setup(client):
    client.add_cog(CROInfo(client))