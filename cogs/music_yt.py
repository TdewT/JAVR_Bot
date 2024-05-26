import discord
from discord.ext import commands
import wavelink


class Music_YT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.add_command(self.play,guild=discord.Object(id=692802312720089108))
        bot.tree.add_command(self.leave,guild=discord.Object(id=692802312720089108))
        bot.tree.add_command(self.stop,guild=discord.Object(id=692802312720089108))
        bot.tree.add_command(self.skip,guild=discord.Object(id=692802312720089108))
        bot.tree.add_command(self.pause,guild=discord.Object(id=692802312720089108))
        bot.tree.add_command(self.resume,guild=discord.Object(id=692802312720089108))

    @discord.app_commands.command(name="play", description="Add track to queue")
    async def play(self,interaction: discord.Interaction, search: str):
        track = await wavelink.Playable.search(search)
        if interaction.user.voice.channel:
            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
                await vc.set_volume(100)
            else:
                vc: wavelink.Player = interaction.client.voice_clients[0]
            await interaction.response.send_message(f"Now playing {track[0]}", ephemeral=True)
            if vc.playing:
                await vc.queue.put(track[0])
            else:
                await vc.play(track=track[0])
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
            
    @discord.app_commands.command(name="leave", description="Make the bot leave your channel")
    async def leave(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel: 
            vc: wavelink.Player = interaction.client.voice_clients[0]
            await interaction.response.send_message("I have left the channel", ephemeral=True)
            await vc.disconnect()
    
    @discord.app_commands.command(name="stop", description="Stop current track")
    async def stop(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.client.voice_clients[0]
        await interaction.response.send_message("Stopped the music",ephemeral=True)
        await vc.stop()
        
    @discord.app_commands.command(name="skip", description="Skip current track")
    async def skip(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.client.voice_clients[0]
        await interaction.response.send_message("Skipped to next track", ephemeral=True)
        await vc.skip()
        
    @discord.app_commands.command(name="pause",description="Pause current track")
    async def pause(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.client.voice_clients[0]
        if not vc.paused:
            await interaction.response.send_message("Paused current track", ephemeral=True)
            vc.pause()
        else:
            await interaction.response.send_message("Track is already paused", ephemeral=True) 
            
    @discord.app_commands.command(name="resume", description="Resumes current track")
    async def resume(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.client.voice_clients[0]
        if vc.paused:
            await interaction.response.send_message("Resumed current track", ephemeral=True)
            vc.pause(False)
        else:
            await interaction.response.send_message("Track is not paused", ephemeral=True)  
        
        
        
    
        
        
async def setup(bot):
    await bot.add_cog(Music_YT(bot))