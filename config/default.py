welcome_channel_mess = "New welcome channel has been set"

ban_error_mess = "You don't have permissions to ban a user!"
kick_error_mess = "You don't have permissions to kick a user!"
command_error_mess = "You don't have permissions to do that!"
no_voice_mess = "I'm not connected to a voice channel"
no_destination_mess = "You are not connected to a voice channel"
different_channel_mess = "You have to be in the same voice channel"

loop_on_mess = "Loop is enabled"
loop_off_mess = "Loop is disabled!"

is_paused_mess = "Music has beed paused"
in_not_paused_mess = "Music was not paused"

not_playing_mess = "Music is not playing"

queue_empty_mess = "Queue is empty"

queue_title = "Queue"

def ban_message(member):
    return f"User {member} has just been banned from the server"

def kick_message(member):
    return f"User {member} has just been kicked form the server"

def greeting_mess(member):
    return f"New user has joined the server! It's {member}"

def goodbye_mess(member):
    return f"User has left the server, he's name was {member}"

def queue_len_mess(queue):
    return f"There's currently {len(queue)} tracks in the queue."

def queue_list_mess(song_count):
    return f"Track number: {song_count}"
    
def queue_footter(queue):
    return f"And {len(queue) - 6} more."

