val clientId: String? = System.getenv("spoti_id")
val clientSecret: String? = System.getenv("spoti_secret")
val spDc: String? = System.getenv("spoti_spdc")


AudioPlayerManager playerManager  =  new DefaultAudioPlayerManager ();
// create a new SpotifySourceManager with the default providers, clientId, clientSecret, spDc, countryCode and AudioPlayerManager and register it
playerManager.registerSourceManager(new SpotifySourceManager(null, clientId, clientSecret, spDc, "PL", playerManager));
