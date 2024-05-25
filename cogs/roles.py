import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.add_command(self.role_modify,guild=discord.Object(id=692802312720089108))
        # dict construction "emoji_name":[emoji_id, role_id]
        self.role_info = {"squad":[1243605677063274538,1243594369009713163],"arma3":[1243606971488403590,903684702500700160],"COH2":[1243840205128073286,1243837274349899816],"GTFO":[1243840203869651025,1243837477215670302],\
            "HD2":[1243840208936374354,1243836841720025228],"Ready_or_Not":[1243840201135095839,1243837361889218570],"cs2":[1243840206722044014,1243837029872308224],"dayz":[1243840207892119572,1243837200299200542],"rocket_league":[1243840202489991168,1243837073895460929]}
        

    @discord.app_commands.command(name="role", description="Sends role selection message")
    async def role_modify(self,interaction: discord.Interaction):
        emb = discord.Embed(title="Wybierz jedną z poniższych Emoji aby otrzymać rolę: ", description="<:squad:1243605677063274538>  - Squad \n\
            <:arma3:1243606971488403590>  - Arma 3 \n\
            <:COH2:1243840205128073286>  - Company of Heroes 2 \n\
            <:GTFO:1243840203869651025>  - GTFO \n\
            <:HD2:1243840208936374354>  - HELLDIVEDS 2 \n\
            <:Ready_or_Not:1243840201135095839>  - Ready or Not \n\
            <:cs2:1243840206722044014>  - Counter Strike 2 \n\
            <:dayz:1243840207892119572>  - DayZ \n\
            <:rocket_league:1243840202489991168>  - Rocket League", color=0xFF0080)
        if interaction.channel_id == 1243588381472985179:
            await interaction.response.send_message(embed=emb, ephemeral = False)
            for id in self.role_info.values():
                em = interaction.user.guild.get_emoji(id[0])
                msg = await interaction.original_response()
                await msg.add_reaction(em)
        else:
            await interaction.response.send_message("Nie można użyć tej komendy na tym kanale", ephemeral = True)    
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id==1243588381472985179:
            user = payload.member      
            emo_id = self.role_info.get(payload.emoji.name)
            await user.add_roles(user.guild.get_role(emo_id[1]))
            
  
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id==1243588381472985179:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
            user = await guild.fetch_member(payload.user_id)
            
            role_id = self.role_info.get(payload.emoji.name)
            await user.remove_roles(user.guild.get_role(role_id[1]))
        
                    
async def setup(bot):
    await bot.add_cog(Roles(bot))