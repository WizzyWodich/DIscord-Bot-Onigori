import disnake
from disnake.ext import commands
from support.SettingViev import CategoryViews


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="settings", help="Настройка бота")
    @commands.has_permissions(administrator=True)
    async def settings(self, interaction: disnake.ApplicationCommandInteraction):
        categories = ["Установить канал логирования", "Установить канал приветствия", "Установить автороль", "Сброс данных гильдии"]
        view = CategoryViews(categories=categories)
        embed = disnake.Embed(
            title="<:settings:1275894886910136423> Настройки бота",
            description=f'''** > Здравствуйте. Вы находитесь в найстроках бота для сервера `{interaction.guild.name}`. Выберие категорию:**''',
            color=disnake.Color.blurple()
        )
        
        await interaction.send(embed=embed, view=view, ephemeral=True)
        
        
def setup(bot):
    bot.add_cog(Settings(bot))