import discord
from discord.ext import commands
import mal

class Anime(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        bot.tree.add_command(self.anime,guild=discord.Object(id=692802312720089108))
        
    
    @discord.app_commands.command(name= "anime", description="Search for anime")
    async def anime(self,interaction: discord.Interaction, anime:str, page:int = 0):
        
        search = mal.AnimeSearch(anime)
        
        result = []
        desc = ""
        
        #Show selection menu
        for i in range(page*5,(page*5)+5):
            result.append(search.results[i]) 
        
        for i in range(5):
            desc += f"{i}. {result[i].title}\n"  
        
        embed = discord.Embed(title=f"Found anime for: {anime}", description= desc)
        print("sending embed")
        await interaction.channel.purge(limit = 1)
        msg = await interaction.send(embed=embed)
        
        #Buttons for anime selection
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        await msg.add_reaction('4️⃣')
        await msg.add_reaction('5️⃣')

        #selecting anime
        reaction, user = await self.client.wait_for("reaction_add",timeout = 30.0)
        
        if str(reaction.emoji) == '1️⃣':
            await show_anime(self,interaction,result[0].mal_id)
        if str(reaction.emoji) == '2️⃣':
            await show_anime(self,interaction,result[1].mal_id)
        if str(reaction.emoji) == '3️⃣':
            await show_anime(self,interaction,result[2].mal_id)
        if str(reaction.emoji) == '4️⃣':    
            await show_anime(self,interaction,result[3].mal_id)
        if str(reaction.emoji) == '5️⃣':
            await show_anime(self,interaction,result[4].mal_id)
            
            
#TODO SHOW GENERES       
#Show anime for selected anime 
async def show_anime(self,interaction,id_anime):
    await interaction.channel.purge(limit = 1)
    
    anime = mal.Anime(id_anime)
    
    
    embed=discord.Embed(title=anime.title, url=anime.url, description=anime.synopsis, color=0x06987b)
    embed.set_thumbnail(url=anime.image_url)
    embed.add_field(name="Score", value=anime.score, inline=True)
    embed.add_field(name="Episodes", value=anime.episodes, inline=True)
    embed.add_field(name="Status", value=anime.status, inline=True)
    await interaction.send(embed=embed)
    
    
    
async def setup(client):
    await client.add_cog(Anime(client))
