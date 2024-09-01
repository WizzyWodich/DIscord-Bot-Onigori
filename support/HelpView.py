import disnake, sys
import datetime

class HellpSelectMenu(disnake.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            disnake.SelectOption(
                label="Утилиты",
                emoji="<:Utils:1279071998634364990>"
            ),
            disnake.SelectOption(
                label="Модерация",
                emoji="<:Modaratin:1279071993534353439>"
            ),
            disnake.SelectOption(
                label="Общие команды",
                emoji="<:Users:1279071996914700311>"
            ),
            disnake.SelectOption(
                label="Информация о боте",
                emoji="<:Bot:1279071991747579904>"
            ),
        ]
        
        super().__init__(placeholder="Выберите категорию...", options=options, custom_id="HelpMenu", min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Общие команды":
            embed = UserEmbed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected_option == "Информация о боте":
            embed = BotEmbed(self.bot)
            await embed.fill_embed() 
            view = ButtonServerDevView()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        elif selected_option == "Утилиты":
            embed = UtilsEmbed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected_option == "Модерация":
            embed = ModerationEmbed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"В разработке", ephemeral=True)
            
class UserEmbed(disnake.Embed):
    def __init__(self):
        super().__init__( 
            title="**<:Users:1279071996914700311> Общие команды:**",
            description=(
                "**`/help` - Список всех доступных комманд**\n"\
                "**`/list_promocodes` - Список промокодов**\n"\
                "**`/promocode_details <code>`- Подробно о конкретном промокоде**\n"\
                "**`/use_promocode <code>`- использовать промокод**\n"
                "**`/profile`- Профиль пользователя**\n"\
                "**`/admin_list`- Список администрации сервера**\n"\
                "**`/info_guild`- Исформация о гильдии**\n"
            ),
            color=disnake.Color.blurple()
        )
        self.timestamp = datetime.datetime.now()

class ModerationEmbed(disnake.Embed):
    def __init__(self):
        super().__init__(  
            title="**<:Modaratin:1279071993534353439> Команды для модерирования/администрирования:**",
            description=(
                "**`/user <member>` - Управление пользователем**\n"\
            ),
            color=disnake.Color.blurple()
        )
        self.timestamp = datetime.datetime.now()

class UtilsEmbed(disnake.Embed):
    def __init__(self):
        super().__init__( 
            title="**<:Utils:1279071998634364990> Утилиты:**",
            description=(
                "**`/clear <count>` - Очистить чат**\n"
                "**`/say <title> <description>` - Написать от имени бота**\n"\
                "**`/add_admin <member>`- Добавить в список администраторов**\n"\
                "**`/del_admin <member>`- Удалить из списка администраторов**\n"\
                "**`/profile`- Профиль пользователя**\n"\
                "**`/admin_list`- Список администрации сервера**\n"\
            ),
            color=disnake.Color.blurple()
        )
        self.timestamp = datetime.datetime.now()

class BotEmbed(disnake.Embed):
    def __init__(self, bot):
        super().__init__(
            title="**<:Utils:1279071998634364990> Информация о боте:**",
            description="",
            color=disnake.Color.blurple()
        )
        self.bot = bot
        self.timestamp = datetime.datetime.now()

    async def fill_embed(self):
        app_info = await self.bot.application_info()
        owner = app_info.owner
        bot_name = app_info.name
        bot_id = app_info.id
        disnake_version = disnake.__version__
        python_version = sys.version

        self.description = (
            f"**`Название бота:` {bot_name}**\n"
            f"**`ID бота:` {bot_id}**\n\n"
            f"**`Python version:` {python_version}**\n"
            f"**`Disnake version:` {disnake_version}**\n\n"
            f"**`Создатель бота:` {owner}**\n"
        )

class ButtonServerDev(disnake.ui.Button):
    def __init__(self, label: str, url: str):
        super().__init__(label=label, style=disnake.ButtonStyle.url, url=url)

class ButtonServerDevView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        # Добавляем нашу кастомную кнопку с ссылкой на сервер в вид
        self.add_item(ButtonServerDev(label="Сервер техподдержки", url="https://discord.gg/upBYJWTY67"))

class HellpMenuViews(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.add_item(HellpSelectMenu(self.bot))

        
