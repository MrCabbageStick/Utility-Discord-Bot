from discord import Cog, Bot, TextChannel, command, ApplicationContext, Message, User

from pin_archivist.pin_archivist_config import PinArchivistConfig
from utils.configHandler import ConfigHandler


class PinArchivist(Cog):
    channelsFetched: bool = False

    def __init__(self, bot: Bot, config: PinArchivistConfig):
        self.bot = bot
        self.config = config


    @command(name="archive_pins")
    async def archivePinsCommand(self, ctx: ApplicationContext, archive_channel: TextChannel):

        if ctx.author.id != ctx.guild.owner_id and not ctx.author.id in self.config.authorizedUserIds:
            await ctx.response.send_message("You are not authorized to use this command")
            return

        pins: list[Message] = await ctx.channel.pins()

        archivedCount = 0
        errorCount = 0

        getMessageText = lambda: f"Started archiving pins...\n:file_cabinet: Archived: {archivedCount}\n:x: Skipped: {errorCount}"

        statusMessage: Message = await ctx.response.send_message(getMessageText(), ephemeral=True)

        for pin in pins:
            try:
                # memeAuthor = ":alien:" if len(pin.mentions) < 1 else pin.mentions[0].jump_url
                # preamble = f"Mem dnia <t:{int(pin.created_at.timestamp())}:d> od {memeAuthor}\n"
                content: str = pin.content if len(pin.content) <= 2000 else pin.content[0:2000]
                message: Message = await archive_channel.send(
                    content=content,
                    files=[await attachment.to_file() for attachment in pin.attachments],
                    silent=True
                )
                await pin.unpin(reason=f":file_cabinet: Pin archived as: {message.jump_url}")

                archivedCount += 1

                try:
                    await statusMessage.edit(content=getMessageText())
                except:
                    pass

            except:
                errorCount += 1

        try:
            await statusMessage.edit(content=f"{getMessageText()}\nArchiving finished")
        except:
            pass


    @command(name="authorize_user")
    async def authorizeUserCommand(self, ctx: ApplicationContext, user: User):

        if ctx.author.id != ctx.guild.owner_id:
            await ctx.response.send_message("You are not authorized to use this command.\nThis command can only be executed by the server owner", ephemeral=True)
            return

        self.config.authorizedUserIds.append(user.id)
        ConfigHandler.setPinArchivistConfig(self.config)

        await ctx.response.send_message(f":loudspeaker: Added {user} to authorized users", ephemeral=True)

