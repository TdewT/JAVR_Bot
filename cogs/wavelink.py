import wavelink
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class Wavelink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload):
        print(f"Node {payload.node!r} is ready!")
        
        
async def setup(bot):
    await bot.add_cog(Wavelink(bot))