import discord
from discord.ext import commands
from discord import Member
import config.javr as conf
    
    
class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.command()
    async def embed(self, ctx,abc=None):
        embed = discord.Embed(title="Dog", url="https://google.com", description="We love dogs", color=0xffc0cb)
        #embed.set_author(name="Arisen", url="https://shinden.pl/user/536995-arisen123", icon_url="https://cdn.discordapp.com/attachments/592003831823597636/1143954719153336350/image.png")
        embed.set_author(name=ctx.author.display_name, url="https://shinden.pl/user/536995-arisen123", icon_url=ctx.author.avatar)
        #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/592003831823597636/1143954719153336350/image.png")
        embed.set_thumbnail(url=abc)
        embed.add_field(name="Field 1", value=" value 1", inline=True)
        embed.add_field(name="Field 2", value=" value 2", inline=True)
        embed.add_field(name="Field 3", value=" value 3", inline=False)
        embed.set_footer(text="Ending text")
        await ctx.send(embed=embed)
        
        
        
        
async def setup(bot):
    await bot.add_cog(Testing(bot))