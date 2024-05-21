welcome_channel_mess = "Nowa komora segregacji została ustanowiona"

ban_error_mess = "Nie masz uprawnien aby przedwcześnie stracić skazańca!"
kick_error_mess = "Nie masz uprawnien aby odesłać kogoś z obozu!"
command_error_mess = "Nie masz uprawnien do tego działania!"
no_voice_mess = "Nie jestem w żadnej komorze"
no_destination_mess = "Wejdź najpierw do komory"
different_channel_mess = "Musisz być ze mną w komorze"

loop_on_mess = "Zapętlenie włączone!"
loop_off_mess = "Zapętlenie wyłączone!"

is_paused_mess = "Odtwarzanie jest już zatrzymane"
in_not_paused_mess = "Odtwarzanie nie było zatrzymane"

not_playing_mess = "Żadna muzyka nie jest odtwarzana"

queue_empty_mess = "Kolejka jest pusta"

queue_title = "Kolejka"


def ban_message(member):
    return f"Skazaniec {member} został przedwczesie stracony"


def kick_message(member):
    return f"Skazaniec {member} został przymusowo odesłany z obozu"


def greeting_mess(member):
    return f"Kolejna ofiara pojawiła się w obozie! Jest to {member}"


def goodbye_mess(member):
    return f"Kolejny straceniec opuścił ten świat.. Był nim {member}"


def queue_len_mess(queue):
    return f"Kolejka zawiera obecnie {len(queue)} utwory."


def queue_list_mess(song_count):
    return f"Numer pozycji: {song_count}"


def queue_footter(queue):
    return f"Oraz {len(queue) - 6} więcej."
