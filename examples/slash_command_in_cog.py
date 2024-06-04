import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.add_command(self.test,guild=discord.Object(id=692802312720089108))

    @discord.app_commands.command(name="test", description="test command")
    async def test(self,interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Hello {name}! It works!")
    
        
async def setup(bot):
    await bot.add_cog(Test(bot))