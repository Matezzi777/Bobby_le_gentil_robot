#==================== INITIALISATION ====================
import discord
from discord.ext import commands
from config import VERSION, ID_ADMIN

#========================= BOT ==========================
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), description=f"Bobby v{VERSION}", help_command=None)

#==================== COLOURS & INFOS ===================
BOT_EMBED_RGB = discord.Colour.from_rgb(59, 149, 212)

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
class ErrorEmbed(discord.Embed):
    def __init__(self, *, colour=discord.Colour.red(), color=discord.Colour.red(), title="ERROR", type='rich', url=None, description=None, timestamp=None) -> None:
        super().__init__(
            colour=colour,
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp
            )
        self.set_footer(text=f"Bobby v{VERSION}")
class SuccessEmbed(discord.Embed):
    def __init__(self, *, colour=discord.Colour.green(), color=discord.Colour.green(), title="ERROR", type='rich', url=None, description=None, timestamp=None) -> None:
        super().__init__(
            colour=colour,
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp
            )
        self.set_footer(text=f"Bobby v{VERSION}")

#======================== MODALS ========================
class FeedbackForm(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="FEEDBACK")
        self.add_item(discord.ui.InputText(label="NAME", style=discord.InputTextStyle.short, placeholder="Name your suggestion !", min_length=3, max_length=50, required=True))
        self.add_item(discord.ui.InputText(label="DESCRIPTION", style=discord.InputTextStyle.long, placeholder="Tell me more about your idea...", min_length=20, max_length=None, required=True))

    async def callback(self, interaction : discord.Interaction):
        admin : discord.User = interaction.guild.get_member(ID_ADMIN)
        name = self.children[0].value
        description = self.children[1].value
        embed_response = BotEmbed(title="FEEDBACK SENT", description="You can take a look at the suggestion you sent :", colour=discord.Colour.green())
        embed_response.add_field(name=f"{name}", value=f"{description}", inline=False)
        embed_response.add_field(name=f"Thanks for your suggestion !", value="", inline=False)
        embed_log = BotEmbed(title="NEW SUGGESTION RECEIVED", description=f"New suggestion made by **@{interaction.user.name}** from **{interaction.guild.name}**.")
        embed_log.add_field(name="NAME :", value=f"{name}", inline=False)
        embed_log.add_field(name="DETAILS :", value=f"{description}", inline=False)
        await admin.send(embed=embed_log)
        await interaction.response.send_message(embed=embed_response, ephemeral=True)