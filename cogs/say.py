import disnake
from disnake.ext import commands
import datetime

class AdminMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="say", description="Отправить сообщение от имени бота с титульником, описанием и изображением/гифкой.", dm_permission=False)
    @commands.has_permissions(administrator=True)
    async def send_message(self, interaction: disnake.AppCommandInteraction,
                           channel: disnake.TextChannel = commands.Param(description="Канал для отправки сообщения"),
                           title: str = commands.Param(description="Титульник сообщения"),
                           description: str = commands.Param(description="Описание сообщения"),
                           image_url: str = commands.Param(default=None, description="URL изображения или гифки")):
        # Создание Embed сообщения
        embed = disnake.Embed(title=title, description=description, color=0xFFA500)

        # Добавление изображения/гифки, если URL предоставлен
        if image_url:
            embed.set_image(url=image_url)

        # Добавление времени отправки в нижнюю часть
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed.set_footer(text=f"Отправлено: {current_time}")

        # Отправка сообщения в указанный канал
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Сообщение успешно отправлено в канал {channel.mention}.")
        else:
            await interaction.response.send_message("Вы не указали канал для отправки сообщения.", ephemeral=True)

# Функция для установки кода
def setup(bot):
    bot.add_cog(AdminMessage(bot))
