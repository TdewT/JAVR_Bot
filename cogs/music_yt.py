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
    async def play(self,interaction: discord.Interaction, youtube: str = None, spotify: str = None):
        if youtube != None:
            query: wavelink.Search = await wavelink.Playable.search(youtube)
        if spotify:
            await interaction.response.send_message("Spotify is not yet supported")
        #print(type(query))
        #print("------------")
        #print(query[0])
        if interaction.user.voice.channel:
            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
                await vc.set_volume(100)
            elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
                vc: wavelink.Player = interaction.client.voice_clients[0]
                await vc.move_to(interaction.user.voice.channel)
            else:
                vc: wavelink.Player = interaction.client.voice_clients[0]
            
            
            if type(query) == list:    
                if vc.playing:
                    await vc.queue.put(query[0])
                else:
                    await vc.play(track=query[0])
                    await interaction.response.send_message(f"Now playing {track[0]}", ephemeral=True)
            elif type(query) == wavelink.tracks.Playlist:
                if vc.playing:
                    for track in query:
                       await vc.queue.put(track)
                else:
                    await vc.play(query[0])
                    for i in range(1,len(query)):
                        await vc.queue.put(query[i])
                    
            else:
                if vc.playing:
                    await vc.queue.put(query)
                else:
                    await vc.play(track=query)
                    await interaction.response.send_message(f"Now playing {query[0]}", ephemeral=True)
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
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
        
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
            
    #@commands.Cog.listener()
    #async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        if not payload.player.queue.is_empty:
            track = payload.player.queue.get()
            await payload.player.play(track)

        
        
        
    
        
        
async def setup(bot):
    await bot.add_cog(Music_YT(bot))