import discord
from discord.ext import commands
import wavelink
from wavelink import TrackEventPayload
import config.javr as conf

        
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#    if (ctx.author.voice):
#        channel = ctx.message.author.voice.channel
#        if (ctx.voice_client):
#            await ctx.guild.voice_client.disconnect()
#        await channel.connect()

    
    current = None    
    @commands.command()
    async def play(self,ctx: commands.Context, *, search: wavelink.YouTubeTrack):
      
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player,self_deaf=True)
            await vc.set_volume(100)
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            vc: wavelink.Player = ctx.voice_client
            await vc.move_to(ctx.author.voice.channel)
        else:
            vc: wavelink.Player = ctx.voice_client        
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            global current
            current = search
        else:
            vc.queue.put(search)
          
        global temp
        temp = ctx
        
        vc.ctx = ctx
        setattr(vc, "loop", False)
    
    
        
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload):
        global current
        ctx = temp
        vc: wavelink.Player = ctx.voice_client
        if vc.loop:
            return await vc.play(current)
        next_song = vc.queue.get()
        current = next_song
        await vc.play(next_song)
    
        
        
    @commands.command()
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send(conf.no_voice_mess)
        elif not ctx.author.voice:
            return await ctx.send(conf.no_destination_mess)
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send(conf.different_channel_mess)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        try:
            if vc.loop == True:
                vc.loop = False
            else:
                vc.loop = True
        except Exception:
            setattr(vc, "loop", False)
        
        if vc.loop:
            return await ctx.send(conf.loop_on_mess)
        else:
            return await ctx.send(conf.loop_off_mess)
        
        
    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send(conf.no_voice_mess)
        elif not ctx.author.voice.channel:
            return await ctx.send(conf.no_destination_mess)
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send(conf.different_channel_mess)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if vc.is_paused():
            return await ctx.send(conf.is_paused_mess)
        else:
            await vc.pause()
    
    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send(conf.no_voice_mess)
        elif not ctx.author.voice.channel:
            return await ctx.send(conf.no_destination_mess)
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send(conf.different_channel_mess)
        else:
            vc: wavelink.Player = ctx.voice_client   
            
        if vc.is_paused():
            await vc.resume()
        else:
            return await ctx.send(conf.in_not_paused_mess)
        
    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send(conf.no_voice_mess)
        elif not ctx.author.voice.channel:
            return await ctx.send(conf.no_destination_mess)
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send(conf.different_channel_mess)
        else:
            vc: wavelink.Player = ctx.voice_client 
            
        if vc.is_playing():
            vc.queue.clear()
            await vc.stop()
        else:
            await ctx.send(conf.not_playing_mess)            
        
        
    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send(conf.no_voice_mess)
        elif not ctx.author.voice.channel:
            return await ctx.send(conf.no_destination_mess)
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send(conf.different_channel_mess)
        else:
            vc: wavelink.Player = ctx.voice_client
            
        if vc.queue.is_empty:
            return await ctx.send(conf.queue_empty_mess)
        
        
        queue = vc.queue.copy()
        song_count = 0
        em = discord.Embed(title=conf.queue_title, color=0xffc0cb, description=conf.queue_len_mess(queue=queue))
        if len(queue) <= 6:   
            for song in queue:
                song_count += 1
                em.add_field(name=conf.queue_list_mess(song_count=song_count), value=f"{song.title}")
        else:
            for song in queue:
                song_count += 1
                if song_count <= 6:
                    em.add_field(name=conf.queue_list_mess(song_count=song_count), value=f"{song.title}")
            em.set_footer(text=conf.queue_footter(queue=queue))
        
        await ctx.send(embed = em)
            
        

    @commands.command()
    async def skip(self,ctx):
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send(conf.not_playing_mess)
            if vc.queue.is_empty:
                return await vc.stop()
            next_song = vc.queue.get()
            await vc.play(next_song)
            if vc.is_paused():
                await vc.resume()
        else:
            await ctx.send(conf.no_voice_mess)
        


    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        if not ctx.voice_client:
            return await ctx.send(conf.no_voice_mess)
        else:
            vc: wavelink.Player = ctx.voice_client
            await vc.disconnect()




    
    
async def setup(bot):
    await bot.add_cog(Music(bot))