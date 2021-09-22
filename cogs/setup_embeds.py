import discord
from discord.ext import commands, tasks
import json
import main

class SetupEmbeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="setup", help='!setup | Setup Updating Embeds in current channel')
    async def setup(self, ctx):
        server_id = ctx.guild.id
        server_name = ctx.guild.name
        guild_exists = main.setup_guild(server_id, server_name)
        if guild_exists:
            guild = main.get_guild(server_id)

            # Price Embed
            await self.client.http.delete_message(int(guild['priceChannel']), int(guild['priceEmbed']))
            em = discord.Embed(
                title="Setup Message",
                description="Setup Description",
                color=discord.Color.purple()
            )
            em.add_field(name="Setup Name", value="Setup Value")
            new_message = await ctx.send(embed=em)
            main.setup_price_embed(server_id, new_message.id, ctx.channel.id)

            # Blockchain Embed
            await self.client.http.delete_message(int(guild['blockchainChannel']), int(guild['blockchainEmbed']))
            em1 = discord.Embed(
                title="Setup Message",
                description="Setup Description",
                color=discord.Color.purple()
            )
            em.add_field(name="Setup Name", value="Setup Value")
            new_message = await ctx.send(embed=em1)
            main.setup_blockchain_embed(server_id, new_message.id, ctx.channel.id)
        else:
            # Price Embed
            em = discord.Embed(
                title="Setup Message",
                description="Setup Description",
                color=discord.Color.purple()
            )
            em.add_field(name="Setting Up Data", value="Please allow up to 10 seconds for data to populate")
            new_message = await ctx.send(embed=em)
            main.setup_price_embed(server_id, new_message.id, ctx.channel.id)

            # Blockchain Embed
            em = discord.Embed(
                title="Setup Message",
                description="Setup Description",
                color=discord.Color.purple()
            )
            em.add_field(name="Setting Up Data", value="Please allow up to 10 seconds for data to populate")
            new_message = await ctx.send(embed=em)
            main.setup_blockchain_embed(server_id, new_message.id, ctx.channel.id)

def setup(client):
    client.add_cog(SetupEmbeds(client))
