import requests, bs4, asyncio, lxml
from Resources.config import CRO_URL, YUM_URL
from Resources.setup import BOT_TOKEN
import discord, json, os
from discord.ext import commands, tasks
from discord.utils import get

prefix = '!'
client = commands.Bot(command_prefix=prefix)

# Cogs
#region Cog Setup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded: {filename[:-3]}')
#endregion

# Loops
#region CRO Price Embed Loop
async def cro_price_embed():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            coin = get_coin("CRO")
            price = coin['price']
            price_change = coin['priceChange']
            price_low = coin['priceLow']
            price_high = coin['priceHigh']
            trading_volume = coin['tradingVolume']

            color = discord.Color.light_grey()
            if float(price_change) >= 0.00:
                color = discord.Color.green()
            else:
                color = discord.Color.red()

            EMPTY = '\u200b'

            em = discord.Embed(
                title='[CRO] Crypto.com Coin',
                description='Live price data and information',
                color=color,
                url="https://coinmarketcap.com/currencies/crypto-com-coin/"
            )

            em.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/64x64/3635.png')
            em.set_footer(text='Updated every few seconds')
            em.add_field(name='Market Price', value=f'${price}')

            em.add_field(name=EMPTY, value=EMPTY, inline=True)

            em.add_field(name='24h Change', value=f'{float(price_change) * 100}%', inline=True)
            em.add_field(name='24h Low/High', value=f'${price_low} / ${price_high}', inline=True)
            em.add_field(name='Trading Volume', value=f'${trading_volume}', inline=False)

            em.set_image(url="https://cdn.discordapp.com/attachments/883439585978384414/888884490921992263/cmc.png")

            guilds = get_guilds()
            for guild_id in guilds:
                current_guild = guilds[guild_id]
                message = await client.get_channel(int(current_guild["priceChannel"])).fetch_message(int(current_guild["priceEmbed"]))
                await message.edit(embed=em)
                await asyncio.sleep(2)
            if guilds == {}:
                await asyncio.sleep(5)
        except Exception as e:
            print(e)
async def get_cro_exchange():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            economic = get_economic()
            response = requests.get(CRO_URL)
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            price = economic['economic']['usdPriceCurrent']
            price_change = economic['economic']['usdPriceChange']
            price_low = soup.find_all('div', {'class': 'sc-16r8icm-0 fmPyWa'})[0].find('tbody').findAll('tr')[2].find('td').findAll('div')[0].text
            price_high = soup.find_all('div', {'class': 'sc-16r8icm-0 fmPyWa'})[0].find('tbody').findAll('tr')[2].find('td').findAll('div')[1].text
            trading_volume = soup.find_all('div', {'class': 'sc-16r8icm-0 fmPyWa'})[0].find('tbody').findAll('tr')[3].find('td').find('span').text

            with open("db.json", "r") as f:
                data = json.load(f)
            data["Coins"]["CRO"]["price"] = str(price)
            data["Coins"]["CRO"]["priceChange"] = str(price_change)
            data["Coins"]["CRO"]["priceLow"] = price_low.replace("$", "").replace(" ", "").replace("/", "")
            data["Coins"]["CRO"]["priceHigh"] = price_high.replace("$", "")
            data["Coins"]["CRO"]["tradingVolume"] = trading_volume.replace("$", "")
            with open("db.json", "w") as j:
                json.dump(data, j, indent=4)
            await asyncio.sleep(5)

        except Exception as e:
            print(e)
            await asyncio.sleep(5)
#endregion
#region Blockchain Info
async def blockchain_info_embed():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            chain = get_blockchain("CRO")
            name = chain['name']
            website = chain['website']
            block_height = chain['blockHeight']
            block_time = chain['blockTime']
            bonded_tokens = chain['bondedTokens']
            total_accounts = chain['totalAccounts']
            total_tx = chain['totalTx']
            total_delegators = chain['totalDelegators']
            inflation_rate = chain['inflationRate']
            total_supply = chain['totalSupply']
            current_avg_apy = chain['currentAvgAPY']

            EMPTY = '\u200b'

            divided_block_time = float(block_time)/1000

            em = discord.Embed(
                title=name,
                description="On-Chain Information for Crypto.org Chain",
                color=discord.Color.blue(),
                url=website
            )

            em.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/64x64/3635.png')
            em.set_footer(text='On-Chain Information provided by Yummy Explorer', icon_url='https://next-explorer.yummy.capital')
            em.set_image(url='https://cdn.discordapp.com/attachments/850427909326897162/890276595791712266/crochain.png')

            em.add_field(name='Block Height', value=block_height, inline=True)
            em.add_field(name='Average Block Time', value=f'{divided_block_time} sec', inline=True)
            em.add_field(name='Total Txs', value=f'{total_tx}', inline=True)

            em.add_field(name=EMPTY, value=EMPTY, inline=False)

            em.add_field(name="Delegated CRO", value=str(round(float(bonded_tokens), 2)), inline=True)
            em.add_field(name="Total Delegators", value=total_delegators, inline=True)
            em.add_field(name="Current % APY", value=f'{round(float(current_avg_apy), 2)}%')

            em.add_field(name=EMPTY, value=EMPTY, inline=False)

            em.add_field(name='Total Accounts', value=f'{total_accounts}', inline=True)
            em.add_field(name='Total Supply', value=f'{round(float(total_supply), 0)} CRO', inline=True)
            em.add_field(name='Inflation Rate', value=f'{round(float(inflation_rate) * 100, 2)}%', inline=True)

            guilds = get_guilds()
            for guild_id in guilds:
                current_guild = guilds[guild_id]
                message = await client.get_channel(int(current_guild["blockchainChannel"])).fetch_message(int(current_guild["blockchainEmbed"]))
                await message.edit(embed=em)
                await asyncio.sleep(2)
            if guilds == {}:
                await asyncio.sleep(5)

        except Exception as e:
            print(e)
async def get_cro_chain_info():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            blocks_response = requests.get(f'{YUM_URL}/blocks?limit=5')
            stats_response = requests.get(f'{YUM_URL}/stats')
            economic_response = get_economic()

            blocks = blocks_response.json()
            stats = stats_response.json()
            economic = economic_response
            #chain = get_blockchain("CRO")

            block_height = str(blocks['blocks'][0]['height'])
            block_time = str(stats['stats']['averageBlockTime']['milliseconds'])
            bonded_tokens = str(int(economic['economic']['bonded']['amount']) / 100000000)
            total_accounts = str(stats['stats']['accounts'])
            total_tx = str(stats['stats']['txs'])
            total_delegators = str(stats['stats']['delegators'])
            inflation_rate = str(economic['economic']['inflation'])
            total_supply = str(economic['economic']['supply'])
            current_avg_apy = str(economic['economic']['apy'] * 100)

            with open("db.json", "r") as f:
                data = json.load(f)

            data['Blockchains']['CRO']['blockHeight'] = block_height
            data['Blockchains']['CRO']['blockTime'] = block_time
            data['Blockchains']['CRO']['bondedTokens'] = bonded_tokens
            data['Blockchains']['CRO']['totalAccounts'] = total_accounts
            data['Blockchains']['CRO']['totalTx'] = total_tx
            data['Blockchains']['CRO']['totalDelegators'] = total_delegators
            data['Blockchains']['CRO']['inflationRate'] = inflation_rate
            data['Blockchains']['CRO']['totalSupply'] = total_supply
            data['Blockchains']['CRO']['currentAvgAPY'] = current_avg_apy

            with open('db.json', 'w') as j:
                json.dump(data, j, indent=4)
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
#endregion
#region Change Status Loop
async def change_status():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            data = get_coin("CRO")
            price = data['price']
            price_change = data['priceChange']
            price_high = data['priceHigh']
            price_low = data['priceLow']
            rotating = [f'1 CRO = ${price}', f'24h Change: {float(price_change) * 100}%', f'24h High: ${price_high}', f'24h Low: ${price_low}']
            for i in rotating:
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=i))
                await asyncio.sleep(4)
        except Exception as e:
            print(e)
#endregion

# Helper Functions used throughout application
#region Helper Functions
def get_economic():
    response = requests.get(f'{YUM_URL}/economic')
    return response.json()

def get_coin(coin_name):
    with open("db.json", "r") as f:
        data = json.load(f)
    return data["Coins"][coin_name]

def get_blockchain(blockchain_name):
    with open("db.json", "r") as f:
        data = json.load(f)
    return data["Blockchains"][blockchain_name]

def get_guilds():
    with open('db.json', 'r') as f:
        data = json.load(f)
    return data['Guilds']

def get_guild(guild_id):
    with open('db.json', 'r') as f:
        data = json.load(f)
    return data["Guilds"][str(guild_id)]

def setup_guild(guild_id, guild_name):
    with open("db.json", 'r') as f:
        data = json.load(f)
    for key in data["Guilds"]:
        if str(guild_id) == key:
            return True
    data["Guilds"][str(guild_id)] = {
        "name": guild_name,
        "priceChannel": "",
        "priceEmbed": "",
        "blockchainChannel": "",
        "blockchainEmbed": ""
    }
    with open('db.json', 'w') as j:
        json.dump(data, j, indent=4)
        return False

def setup_price_embed(guild_id, message_id, channel_id):
    with open("db.json", 'r') as f:
        data = json.load(f)
    data["Guilds"][str(guild_id)]["priceEmbed"] = str(message_id)
    data["Guilds"][str(guild_id)]["priceChannel"] = str(channel_id)
    with open('db.json', 'w') as j:
        json.dump(data, j, indent=4)

def setup_blockchain_embed(guild_id, message_id, channel_id):
    with open("db.json", 'r') as f:
        data = json.load(f)
    data["Guilds"][str(guild_id)]["blockchainEmbed"] = str(message_id)
    data["Guilds"][str(guild_id)]["blockchainChannel"] = str(channel_id)
    with open('db.json', 'w') as j:
        json.dump(data, j, indent=4)
#endregion

# Important Bot Setup Event
#region Important Bot
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="w/ Crypto.com"))
    print("Bot is online")
#endregion

# Runs Bot
#region Bot Loops and Run Tasks
client.loop.create_task(get_cro_exchange())
client.loop.create_task(get_cro_chain_info())
client.loop.create_task(change_status())
client.loop.create_task(cro_price_embed())
client.loop.create_task(blockchain_info_embed())
client.run(BOT_TOKEN)
#endregion
