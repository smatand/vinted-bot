from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_CONNSTRING = os.getenv("MONGODB_CONNSTRING")

VINTED_URL = os.getenv("VINTED_URL")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_ROOM_ID = os.getenv("DISCORD_ROOM_ID")
