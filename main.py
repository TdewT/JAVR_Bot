import asyncio
import discord

from discord.ext import commands
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()

bot = commands.Bot(command_prefix="po ", intents = discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=discord.Activity(type=discord.ActivityType.competing, name=" Wszyscy zginiemy"))
    print(f"{bot.user} is now online!")
    print("--------------------------")
    bot.loop.create_task(connect_nodes())
    await bot.tree.sync(guild=discord.Object(id=692802312720089108))
    #await bot.tree.sync(guild=discord.Object(id=1143475298441113671))
    print("Commands are now synced!")


async def connect_nodes():
    await bot.wait_until_ready()
    node: wavelink.Node = wavelink.Node(identifier='JAVR_Argentino', uri='http://localhost:2333',
                                        password=os.getenv("lavalink_pass"), client=bot)
    await wavelink.Pool.connect(nodes=[node])


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename[:-3] != "testing":
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Extension: {filename} has been loaded")
            #else:
                #await bot.load_extension(f"cogs.testing")
                #print(f"Extension: {filename} has been loaded")



async def main():
    await load()
    await bot.start(os.getenv("TOKEN"))


asyncio.run(main())
