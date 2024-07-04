from utils.configHandler import ConfigHandler
from pathlib import Path
from bot import UtilBot
from dotenv import load_dotenv
import os

ConfigHandler.loadConfig(Path("./config.toml"))

bot = UtilBot(ConfigHandler.getPinArchivistConfig())

if __name__ == "__main__":
    load_dotenv()
    bot.run(token=os.getenv("TOKEN"))