import os
from dotenv import load_dotenv
import subprocess

# Load the .env file
load_dotenv()

# Get the Lavalink server's password, spotify's clientID, SecretClientID and SpDc from the environment variables
lavalink_password = os.getenv('LAVALINK_PASS')
spoti_id = os.getenv('spoti_id')
spoti_secret = os.getenv('spoti_secret')
spoti_spdc = os.getenv('spoti_spdc')

# Start the Lavalink server
subprocess.Popen(['java', '-jar', 'Lavalink.jar'])
