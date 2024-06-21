import discord
from discord.ext import commands
import wavelink


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stopped = False
        # Load commands for bot to use on a server that was specified by ID
        commands = [self.play, self.leave, self.stop, self.skip,
                    self.pause, self.resume, self.clear, self.queue]
        for command in commands:
            bot.tree.add_command(
                command, guild=discord.Object(id=692802312720089108))

    async def player_join(user, guild, client):
        # Check if bot is already connected
        if not guild.voice_client:
            # If bot is not connected to any channel, define new Player and join user's channel
            vc: wavelink.Player = await user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            await vc.set_volume(100)
        # Check if bot is on the same channel a user
        elif guild.voice_client.channel != user.voice.channel:
            # If bot is on another channel, define Player as the previously created one and move to the user's channel
            vc = client.voice_clients[0]
            await vc.move_to(user.voice.channel)
        else:
            # If the bot is already on user's channel, define Player as the previously created one
            vc = client.voice_clients[0]
        return vc

    # Create embed containing tracks form the queue
    @staticmethod
    def create_queue_embed(queue):
        queue_list = "\n".join([f"{song.title} - {(song.length // 60000)}:{
                               (song.length // 1000) % 60:02}" for song in queue[:5]])

        desc = f"🎵 **Next Up:**\n{queue_list}\nAnd {
            len(queue)-5 if len(queue)-5 > 0 else 'nothing'} more."

        emb = discord.Embed(title="Music Queue", description=desc)
        return emb

    @staticmethod
    def check_channel(user, client):
        if user.voice.channel == client.voice_clients[0].channel:
            # If user is in the same channel, define Player as previously created one, and disconnect from the channel
            vc = client.voice_clients[0]
            return vc
        else:
            return None

    # TODO make messages in similar style to other bots
    @discord.app_commands.command(name="play", description="Add track to queue")
    async def play(self, interaction: discord.Interaction, search: str = None):
        # Check if user used search for YouTube or Spotify
        if not search:
            query = None
        elif "spotify" in search:
            # Make query based on Spotify shared link
            query: wavelink.Search = await wavelink.Playable.search(search, source="spsearch")
        else:
            # Make query based on YouTube search/shared link
            query: wavelink.Search = await wavelink.Playable.search(search)
        # Check if user is in a voice channel
        if interaction.user.voice.channel:
            # Run function to define Player and connect him to user's channel
            vc = await Music.player_join(interaction.user, interaction.guild, interaction.client)
            # Check if query is empty
            if query and search:
                # If query is a Playlist add all tracks to the queue
                if isinstance(query, wavelink.tracks.Playlist):
                    added: int = await vc.queue.put_wait(query)
                # If query is not a Playlist add first result found by search to the queue
                else:
                    track: wavelink.Playable = query[0]
                    await vc.queue.put_wait(track)
                    added = 1
            elif search and not query:
                added = None
                await interaction.response.send_message("Couldn't find the song", ephemeral=False)
            elif not query:
                if not vc.queue.is_empty:
                    await interaction.response.send_message("Playing first song from the queue")
                added = None

            # Check if the Player is currently playing music
            if not vc.playing:
                # If Player is not playing, play first track from the queue
                if vc.queue.is_empty:
                    await interaction.response.send_message("The queue is empty", ephemeral=False)
                else:
                    await vc.play(vc.queue.get())
            elif not added:
                await interaction.response.send_message("Music is currently playing, add query to place in the queue", ephemeral=True)

            if added:
                # Send message that says how many tracks were added to the queue
                await interaction.response.send_message(f"Added {added} tracks to the queue", ephemeral=False)
        else:
            # Send message that informs user he's not connected to the voice channel
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    @discord.app_commands.command(name="leave", description="Make the bot leave your channel")
    async def leave(self, interaction: discord.Interaction):
        # Run function to check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            # If user is in the same channel, define Player as previously created one, and disconnect from the channel
            await vc.disconnect()
            await interaction.response.send_message("I have left the channel", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    @discord.app_commands.command(name="stop", description="Stop current track")
    async def stop(self, interaction: discord.Interaction):
        # Check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            self.stopped = True
            await vc.stop()
            await interaction.response.send_message("Stopped the music", ephemeral=False)
        else:
            await interaction.response.send_message("You are not in my voice channel", ephemeral=True)

    @discord.app_commands.command(name="clear", description="Clear the queue")
    async def clear(self, interaction: discord.Interaction):
        # Run function to check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            # Check if the queue is empty, If not clear its contents
            if not vc.queue.is_empty:
                await interaction.response.send_message("Queue has been cleared")
                vc.queue.clear()
            else:
                await interaction.response.send_message("Your queue is empty")
        else:
            await interaction.response.send_message("You are not in my voice channel", ephemeral=True)

    @discord.app_commands.command(name="skip", description="Skip current track")
    async def skip(self, interaction: discord.Interaction):
        # Run function to check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            await vc.stop()
            # Check if the queue is empty
            if not vc.queue.is_empty:
                # If the queue is not empty, play next track
                # await vc.play(vc.queue.get())
                await interaction.response.send_message("Skipped to next track", ephemeral=False)
            else:
                await interaction.response.send_message("There's nothing left in the queue")
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    @discord.app_commands.command(name="pause", description="Pause current track")
    async def pause(self, interaction: discord.Interaction):
        # Run function to check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            # Check if Player is paused
            if not vc.paused:
                # If Player is not paused, pause the current track
                await vc.pause(True)
                await interaction.response.send_message("Paused current track", ephemeral=False)
            else:
                await interaction.response.send_message("Track is already paused", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    @discord.app_commands.command(name="resume", description="Resumes current track")
    async def resume(self, interaction: discord.Interaction):
        # Run function to check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            # Check if Player is paused
            if vc.paused:
                # If Player is paused, resume paused track
                await vc.pause(False)
                await interaction.response.send_message("Resumed current track", ephemeral=False)
            else:
                await interaction.response.send_message("Track is not paused", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    # TODO command doesn't work if the bot is not on the channel
    @discord.app_commands.command(name="queue", description="Display queue content")
    async def queue(self, interaction: discord.Interaction):
        # Run function to check if user is in the same channel as bot
        vc = Music.check_channel(interaction.user, interaction.client)
        if vc:
            # Check if the queue is empty and create an embed with queue contents
            if not vc.queue.is_empty:
                emb = Music.create_queue_embed(vc.queue)
                # Send a message with created embed
                await interaction.response.send_message(embed=emb, ephemeral=False)
            else:
                await interaction.response.send_message("Your queue is empty")
        else:
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    # Activates when track starts playing
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        # Get the channel by ID
        bot_txt_channel = self.bot.get_channel(875521178524065792)
        # Send a message with the title of currently playing track
        await bot_txt_channel.send(f"Now playing: {payload.track}")

    # Activates when track ends
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        if not self.stopped:
            vc = payload.player
            await vc.play(vc.queue.get())
        else:
            self.stopped = False

    # Activates when Player is inactive for too long
    @commands.Cog.listener()
    async def on_wavelink_inactive_player(self, player: wavelink.Player):
        await player.disconnect()


async def setup(bot):
    await bot.add_cog(Music(bot))
