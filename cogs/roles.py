import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.add_command(self.role_modify,guild=discord.Object(id=692802312720089108))
        self.emoji_names = ["squad", "arma3"]
        self.role_ids = [1243594369009713163, 903684702500700160]

    @discord.app_commands.command(name="role", description="Sends role selection message")
    async def role_modify(self,interaction: discord.Interaction):
        emb = discord.Embed(title="Wybierz jedną z poniższych Emoji aby otrzymać rolę: ", description="<:squad:1243605677063274538>  - To recieve pings when someone is looking for team to play Squad \n\
            <:arma3:1243606971488403590>  - To recieve pings when someone is looking for team to play Arma 3", color=0xFF0080)
        if interaction.channel_id == 1243588381472985179:
            await interaction.response.send_message(embed=emb, ephemeral = False)
        else:
            await interaction.response.send_message("Nie można użyć tej komendy na tym kanale", ephemeral = True)    
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id==1243588381472985179:
            user = payload.member
            
            #emoji_names = ["squad", "arma3"]
            #role_ids = [1243594369009713163, 903684702500700160]
            for i in range(0,len(self.emoji_names)):
                if payload.emoji.name==self.emoji_names[i]:
                    await user.add_roles(user.guild.get_role(self.role_ids[i]))
  
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id==1243588381472985179:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
            user = await guild.fetch_member(payload.user_id)
            
            #emoji_names = ["squad", "arma3"]
            #role_ids = [1243594369009713163, 903684702500700160]
            for i in range(0,len(self.emoji_names)):
                if payload.emoji.name==self.emoji_names[i]:
                    await user.remove_roles(user.guild.get_role(self.role_ids[i]))
                    

async def setup(bot):
    await bot.add_cog(Roles(bot))