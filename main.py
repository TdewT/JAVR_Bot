import asyncio
import discord

from discord.ext import commands
import os
from dotenv import load_dotenv, dotenv_values
import wavelink



load_dotenv()


#bot = commands.Bot(command_prefix="po ", intents = discord.Intents.all())
bot = commands.Bot(command_prefix="t ", intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Activity(type=discord.ActivityType.competing, name=" Wszyscy zginiemy"))
    print(f"{bot.user} is now online!")
    print("--------------------------")
    bot.loop.create_task(connect_nodes())
    
async def connect_nodes():
    await bot.wait_until_ready()
    node: wavelink.Node = wavelink.Node(id='Project Origin', uri='fsn.lavalink.alexanderof.xyz:2333', password='lavalink')
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    
@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node: {node.id} is ready")
    
    
      

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
    #await bot.start(os.getenv("TOKEN"))
    await bot.start(os.getenv("tester"))
          
    
asyncio.run(main())
            