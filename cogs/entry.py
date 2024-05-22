import discord
from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel = 752201041595859034 #contains channel ID for "komora-segregacji-rasowej"
    

    #send welcome message when new member enters the server
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(self.welcome_channel)
        embed = discord.Embed(title=f"Kolejna ofiara pojawiła się w obozie! Jest to {member}", color=0xffc0cb)
        await channel.send(embed=embed)
        role = discord.utils.get(member.guild.roles, id=752201354591600640)
        await member.add_roles(role)
        

    #send goodbye message when member leaves the server
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel  = self.bot.get_channel(self.welcome_channel)
        embed = discord.Embed(title=f"Kolejny straceniec opuścił ten świat.. Był nim {member}", color=0xffc0cb)
        await channel.send(embed=embed)
    
    
    
            
        
        
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))
