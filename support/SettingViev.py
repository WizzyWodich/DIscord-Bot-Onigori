import disnake
from database.LogsDatabase import LogsDatabase
from database.Welcome_Channel import WelcomeChannel
from database.AutoroleDB import AutoRoleDanabase

logsDB = LogsDatabase()
welcomeDB = WelcomeChannel()
autoroleDB = AutoRoleDanabase()


class CategoryDropDown(disnake.ui.Select):
    def __init__(self, categories):
        options = [
            disnake.SelectOption(label=category, value=category)
            for category in categories
        ]
        super().__init__(placeholder="Выберите категорию...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: disnake.MessageInteraction):
        selected_category = self.values[0]
        
        if selected_category == "Установить канал логирования":
            await self.handle_logging_channel(interaction)
        
        elif selected_category == "Установить канал приветствия":
            await self.handle_welcome_channel(interaction)
        
        elif selected_category == "Установить автороль":
            await self.handle_autorole(interaction)
        
        elif selected_category == "Сброс данных гильдии":
            await self.reset_guild_data(interaction)
        
        else:
            await interaction.response.send_message("**### Ошибка: Возможно категория не поддерживается.**", ephemeral=True)

    async def handle_logging_channel(self, interaction):
        guild_log_channel = await logsDB.get_log_channel(interaction.guild)
        current_log_channel = interaction.guild.get_channel(guild_log_channel) if guild_log_channel else "Не установлен"
        
        text_channels = [channel for channel in interaction.guild.channels if isinstance(channel, disnake.TextChannel)]
        view = LoggingChannelDropdownView(text_channels)
        
        embed = disnake.Embed(
            title="<:settings:1275894886910136423> Настройки бота",
            description=f"** > Вы находитесь в настройках канала логирования для сервера `{interaction.guild.name}`. Выберите канал:**",
            color=disnake.Color.blurple()
        )
        embed.add_field(name="Текущий канал логирования", value=f'`{current_log_channel}`')
        
        await interaction.response.edit_message(embed=embed, view=view)

    async def handle_welcome_channel(self, interaction):
        guild_welcome_channel = await welcomeDB.get_welcome_channel(interaction.guild)
        current_welcome_channel = interaction.guild.get_channel(guild_welcome_channel) if guild_welcome_channel else "Не установлен"
        
        text_channels = [channel for channel in interaction.guild.channels if isinstance(channel, disnake.TextChannel)]
        view = WelcomeChannelDropdownView(text_channels)
        
        embed = disnake.Embed(
            title="<:settings:1275894886910136423> Настройки бота",
            description=f"** > Вы находитесь в настройках канала приветствия для сервера `{interaction.guild.name}`. Выберите канал:**",
            color=disnake.Color.blurple()
        )
        embed.add_field(name="Текущий канал приветствия", value=f'`{current_welcome_channel}`')
        
        await interaction.response.edit_message(embed=embed, view=view)

    async def handle_autorole(self, interaction):
        guild_autorole = await autoroleDB.get_autorole(interaction.guild)
        
        roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
        view = AutoroleDropdownView(roles)
        
        embed = disnake.Embed(
            title="<:settings:1275894886910136423> Настройки бота",
            description=f"** > Вы находитесь в настройках авторолей для сервера `{interaction.guild.name}`. Выберите роль:**",
            color=disnake.Color.blurple()
        )
        embed.add_field(name="Текущая автороль", value=f'`{guild_autorole}`')
        
        await interaction.response.edit_message(embed=embed, view=view)

    async def reset_guild_data(self, interaction):
        if interaction.author == interaction.guild.owner or interaction.author.guild_permissions.administrator:
            await logsDB.remove_log_channel(interaction.guild)
            await welcomeDB.remove_channel(interaction.guild)
            await autoroleDB.remove_autorole(interaction.guild)
            await interaction.response.send_message("### Данные гильдии успешно сброшены.", ephemeral=True)
        else:
            await interaction.response.send_message("### Вы не являетесь владельцем гильдии или администратором.", ephemeral=True)


class LoggingChannelDropdown(disnake.ui.Select):
    def __init__(self, channels):
        options = [
            disnake.SelectOption(label=channel.name, value=str(channel.id))
            for channel in channels
        ]
        super().__init__(placeholder="Выберите канал для логирования...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_channel_id = int(self.values[0])
        selected_channel = interaction.guild.get_channel(selected_channel_id)
        await logsDB.insert_logs_channel(selected_channel, interaction.guild)
        await interaction.response.send_message(f'### Канал для логирования установлен: {selected_channel.name}', ephemeral=True)


class WelcomeChannelDropdown(disnake.ui.Select):
    def __init__(self, channels):
        options = [
            disnake.SelectOption(label=channel.name, value=str(channel.id))
            for channel in channels
        ]
        super().__init__(placeholder="Выберите канал для приветствия...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_channel_id = int(self.values[0])
        selected_channel = interaction.guild.get_channel(selected_channel_id)
        await welcomeDB.add_welcome_channel(interaction.guild, selected_channel)
        await interaction.response.send_message(f'### Канал для приветствия установлен: {selected_channel.name}', ephemeral=True)


class AutoroleDropdown(disnake.ui.Select):
    def __init__(self, roles):
        options = [
            disnake.SelectOption(label=role.name, value=str(role.id))
            for role in roles
        ]
        super().__init__(placeholder="Выберите автороль...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_role_id = int(self.values[0])
        selected_role = interaction.guild.get_role(selected_role_id)
        
        # Перевірка на адміністраторські права
        if selected_role.permissions.administrator:
            await interaction.response.send_message(f'### Нельзя установить роль {selected_role.name} в качестве автороли, так как она имеет администраторские права.', ephemeral=True)
        else:
            await autoroleDB.add_autorole(selected_role, interaction.guild)
            await interaction.response.send_message(f'### Автороль установлена: {selected_role.name}', ephemeral=True)


class CategoryViews(disnake.ui.View):
    def __init__(self, categories):
        super().__init__()
        self.add_item(CategoryDropDown(categories=categories))


class LoggingChannelDropdownView(disnake.ui.View):
    def __init__(self, channels):
        super().__init__()
        self.add_item(LoggingChannelDropdown(channels))
        self.add_item(ButtonBack())


class WelcomeChannelDropdownView(disnake.ui.View):
    def __init__(self, channels):
        super().__init__()
        self.add_item(WelcomeChannelDropdown(channels))
        self.add_item(ButtonBack())


class AutoroleDropdownView(disnake.ui.View):
    def __init__(self, roles):
        super().__init__()
        self.add_item(AutoroleDropdown(roles))
        self.add_item(ButtonBack())


class ButtonBack(disnake.ui.Button):
    def __init__(self):
        super().__init__(label="Назад", style=disnake.ButtonStyle.blurple, custom_id="btBack")

    async def callback(self, interaction: disnake.Interaction):
        # Повторное создание исходного интерфейса настроек
        categories = ["Установить канал логирования", "Установить канал приветствия", "Установить автороль", "Сброс данных гильдии"]
        view = CategoryViews(categories=categories)
        
        embed = disnake.Embed(
            title="<:settings:1275894886910136423> Настройки бота",
            description=f"** > Здравствуйте. Вы находитесь в настройках бота для сервера `{interaction.guild.name}`. Выберите категорию:**",
            color=disnake.Color.blurple()
        )
        await interaction.response.edit_message(embed=embed, view=view)
