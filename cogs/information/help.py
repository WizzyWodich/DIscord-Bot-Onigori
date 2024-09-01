import disnake
import datetime
from disnake.ext import commands
from support.HelpView import HellpMenuViews  # Убедитесь, что путь правильный

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Информация по командам")
    async def help(self, interaction: disnake.ApplicationCommandInteraction):
        view = HellpMenuViews(self.bot)
        
        embed = disnake.Embed(
            title="**Помощь <:Info:1279083167344623677>**",
            description="**Выберите категорию**",
            color=disnake.Color.blurple()
        )
        embed.timestamp = datetime.datetime.now()
        embed.thumbnail = self.bot.user.avatar.url
        await interaction.response.send_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Help(bot))
