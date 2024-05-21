import discord
from discord.ext import commands
import config.javr as conf


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    welcome_channel = 0

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(welcome_channel)
        embed = discord.Embed(title=conf.greeting_mess(member=member), color=0xffc0cb)
        await channel.send(embed=embed)
        

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel  = self.bot.get_channel(welcome_channel)
        embed = discord.Embed(title=conf.goodbye_mess(member=member), color=0xffc0cb)
        await channel.send(embed=embed)
    
    # @commands.command()
    # async def test(self,ctx):
    #     await ctx.send("test")

    @commands.command()
    async def set_welcome_channel(self,ctx: commands.Context, set_id):
        set_id = set_id[2::]
        set_id = set_id[:-1]
        set_id = int(set_id)
        for channel in ctx.guild.text_channels:
            if channel.id == set_id:
                global welcome_channel
                welcome_channel = set_id
                await ctx.send(conf.welcome_channel_mess)
            
        
        
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))
