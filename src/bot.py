from discord import Bot
from pin_archivist.pin_archivist_cog import PinArchivist
from pin_archivist.pin_archivist_config import PinArchivistConfig

class UtilBot(Bot):

    def __init__(self, pinArchivistConfig: PinArchivistConfig):
        super().__init__()

        self.add_cog(PinArchivist(self, pinArchivistConfig))

        @self.event
        async def on_ready():
            print("Ready to protected the sinful craft of meme")