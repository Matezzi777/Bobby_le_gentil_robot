#==================== INITIALISATION ====================
import discord
from discord.ext import commands
from config import VERSION

#========================= BOT ==========================

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), description=f"Bobby v{VERSION}")

#======================== COLOURS =======================
BOT_EMBED_RGB = discord.Colour.from_rgb(128, 5, 5)
#======================== EMBEDS ========================

class BotEmbed(discord.Embed):
    def __init__(self, *, colour=BOT_EMBED_RGB, color=BOT_EMBED_RGB, title="TITLE", type='rich', url=None, description=None, timestamp=None):
        super().__init__(
            colour=colour,
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp)
        self.set_footer(text=f"Bobby v{VERSION}")