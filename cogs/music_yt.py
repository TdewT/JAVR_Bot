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
        bot.tree.add_command(self.clear,guild=discord.Object(id=692802312720089108))
        bot.tree.add_command(self.queue,guild=discord.Object(id=692802312720089108))


    @discord.app_commands.command(name="play", description="Add track to queue")
    async def play(self,interaction: discord.Interaction, youtube: str = None):#, spotify: str = None):
        if youtube != None:
            query: wavelink.Search = await wavelink.Playable.search(youtube)
            
        if interaction.user.voice.channel:
            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
                await vc.set_volume(100)
            elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
                vc: wavelink.Player = interaction.client.voice_clients[0]
                await vc.move_to(interaction.user.voice.channel)
            else:
                vc: wavelink.Player = interaction.client.voice_clients[0]
                
            if isinstance(query, wavelink.tracks.Playlist):
                added: int = await vc.queue.put_wait(query)
            else:
                track: wavelink.Playable = query[0]
                await vc.queue.put_wait(track)
                added = 1
                
            if not vc.playing:
                if vc.queue.is_empty:
                    to_play = track
                else:
                    to_play = vc.queue.get()
                await vc.play(to_play)
                await interaction.response.send_message(f"Now playing {to_play}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Added {added} tracks to the queue")
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
            
    @discord.app_commands.command(name="leave", description="Make the bot leave your channel")
    async def leave(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel: 
            vc: wavelink.Player = interaction.client.voice_clients[0]
            await vc.disconnect()
            await interaction.response.send_message("I have left the channel", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
    
    @discord.app_commands.command(name="stop", description="Stop current track")
    async def stop(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel: 
            vc: wavelink.Player = interaction.client.voice_clients[0]
            await vc.stop()
            await interaction.response.send_message("Stopped the music",ephemeral=True)
        else:
            await interaction.response.send_message("You are not in my voice channel", ephemeral=True)
            
    @discord.app_commands.command(name="clear",description="Clear the queue")
    async def clear(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel:
            vc: wavelink.Player = interaction.client.voice_clients[0]
            if not vc.queue.is_empty:
                await vc.queue.clear()
            await interaction.response.send_message("Queue has been cleared")
        else:
            await interaction.response.send_message("You are not in my voice channel", ephemeral=True)
        
    @discord.app_commands.command(name="skip", description="Skip current track")
    async def skip(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel: 
            vc: wavelink.Player = interaction.client.voice_clients[0]

            await vc.skip()
            await interaction.response.send_message("Skipped to next track", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
        
    @discord.app_commands.command(name="pause",description="Pause current track")
    async def pause(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel: 
            vc: wavelink.Player = interaction.client.voice_clients[0]
            if not vc.paused:
                await vc.pause(True)
                await interaction.response.send_message("Paused current track", ephemeral=True)
            else:
                await interaction.response.send_message("Track is already paused", ephemeral=True) 
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
            
    @discord.app_commands.command(name="resume", description="Resumes current track")
    async def resume(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel: 
            vc: wavelink.Player = interaction.client.voice_clients[0]
            if vc.paused:
                await vc.pause(False)
                await interaction.response.send_message("Resumed current track", ephemeral=True)
            else:
                await interaction.response.send_message("Track is not paused", ephemeral=True) 
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
            
    @discord.app_commands.command(name="queue",description="Display queue content")
    async def queue(self, interaction: discord.Interaction):
        if interaction.user.voice.channel == interaction.client.voice_clients[0].channel:
            vc: wavelink.Player = interaction.client.voice_clients[0]
            await interaction.response.send_message(f"Your queue is: {vc.queue}", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music_YT(bot))