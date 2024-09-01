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
            if image_url.startswith("http://") or image_url.startswith("https://"):
                embed.set_image(url=image_url)
            else:
                await interaction.response.send_message("Некорректный URL изображения. Убедитесь, что URL начинается с http:// или https://", ephemeral=True)
                return

        # Добавление времени отправки в нижнюю часть
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed.set_footer(text=f"Отправлено: {current_time}")

        # Отправка сообщения в указанный канал
        if channel:
            try:
                await channel.send(embed=embed)
                await interaction.response.send_message(f"Сообщение успешно отправлено в канал {channel.mention}.")
            except disnake.Forbidden:
                await interaction.response.send_message("У бота нет прав на отправку сообщений в указанный канал.", ephemeral=True)
            except disnake.HTTPException as e:
                await interaction.response.send_message(f"Произошла ошибка при отправке сообщения: {e}", ephemeral=True)
        else:
            await interaction.response.send_message("Вы не указали канал для отправки сообщения.", ephemeral=True)

# Функция для установки кода
def setup(bot):
    bot.add_cog(AdminMessage(bot))
