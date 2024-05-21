import discord
from discord.ext import commands
from discord import Member
from discord import FFmpegPCMAudio
import config.javr as conf

class Casual(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello There!")
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            if (ctx.voice_client) and not ctx.voice_client == channel:
                await ctx.guild.voice_client.disconnect()
            voice = await channel.connect()
            source = FFmpegPCMAudio('hello.mp3')
            player = voice.play(source)
        else:
            await ctx.send(conf.no_voice_mess)
    
    
    @commands.command()
    async def pobudka(self, ctx: commands.Context, user: discord.Member, *, message=None):
        if user.id == 1143475679510396978:
            await ctx.send("Nie mogę obudzić podanej osoby")
        elif user.id == 299588320541802496:
            await user.send("Wstajemy już 18")
        else:
            for i in range(10):
                await user.send("Wstajemy już 18")

    
async def setup(bot):
    await bot.add_cog(Casual(bot))