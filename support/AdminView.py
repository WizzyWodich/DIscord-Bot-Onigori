import disnake, datetime

from database.UserInfoDatabase import UsersDataBase
from database.RankDatabase import RankDatabase
from database.LogsDatabase import LogsDatabase



logsDB = LogsDatabase()
rankDB = RankDatabase()
userDB = UsersDataBase()


class SelectMenu(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Сменить имя",
                emoji="<:edit:1276842285581205526>"
            ),
            disnake.SelectOption(
                label="Ограничить пользователя в слове",
                emoji="<:mutes:1276842288697446472>"
            ),
            disnake.SelectOption(
                label="Предупредить пользователя",
                emoji="<:warn:1276842528850837586>"
            ),
            disnake.SelectOption(
                label="Забанить пользователя",
                emoji="<:ban:1276842286801485844>"
            ),
            disnake.SelectOption(
                label="Экономика пользователя",
                emoji="<:economy:1276844363942465618>"
            ),
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="adminMenu", min_values=1, max_values=1)

    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Сменить имя":
            await interaction.response.send_modal(ModalRename(self.member))
        elif selected_option == "Ограничить пользователя в слове":
            view =  MuteMenuViews(self.member)
            await interaction.response.edit_message(view=view)
        elif selected_option == "Забанить пользователя":
            await self.member.ban()
            embed = disnake.Embed(
            title="<:ban:1276842286801485844> Пользователь забанен",
            description=f"**Пользователь `{self.member.mention}` был забанен.**",
            color=disnake.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selected_option == "Экономика пользователя":
            view = EconomyMenuViews(self.member)
            await interaction.response.edit_message(view=view)
        elif selected_option == "Предупредить пользователя":
            view =  WarnMenuViews(self.member)
            await interaction.response.edit_message(view=view)
            
            
            
            
class MuteSelect(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Забрать право голоса",
                emoji="<:edit:1276842285581205526>"
            ),
            disnake.SelectOption(
                label="Возобновить право голоса",
                emoji="<:mutes:1276842288697446472>"
            ),
            
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="MuteMenu", min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Забрать право голоса":
            await interaction.response.send_modal(ModalMute(self.member))
        elif selected_option == "Возобновить право голоса":
            if not self.member.current_timeout:
                embed = disnake.Embed(
                    title="Пользователь не в муте",
                    description=f"**Пользователь {self.member.mention} не находится в муте.**",
                    color=disnake.Color.blurple()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await self.member.timeout(until=None, reason=None)
                embed = disnake.Embed(
                    title="<:unmute:1276845250693828651> Размьют",
                    description=f"**Пользователь {self.member.mention} был размьючен.**",
                    color=disnake.Color.blurple()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

            
            
class WarnSelect(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Добавить предупреждение",
                emoji="<:edit:1276842285581205526>"
            ),
            disnake.SelectOption(
                label="Удалить предупреждения",
                emoji="<:mutes:1276842288697446472>"
            ),
            
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="WarnMenu", min_values=1, max_values=1)
            
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Добавить предупреждение":
            await interaction.response.send_modal(ModalWarn(self.member)) 
        elif selected_option == "Удалить предупреждения":
            await interaction.response.send_modal(ModalDeleteWarn(self.member))
            

class EconomySelect(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Монеты",
                emoji="<:coins:1276844360394084383>"
            ),
            disnake.SelectOption(
                label="Рубины",
                emoji="<:gems:1276844361929199690>"
            ),
            disnake.SelectOption(
                label="Опыт",
                emoji="<:score:1276845247443501107>"
            ),
            
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="EconomyMenu", min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Монеты":
            view =  MoneyMenuViews(self.member)
            await interaction.response.edit_message(view=view)
        elif selected_option == "Рубины":
            view =  RubyMenuViews(self.member)
            await interaction.response.edit_message(view=view)
        elif selected_option == "Опыт":
            view =  ScoreMenuViews(self.member)
            await interaction.response.edit_message(view=view)
            
class MoneySelect(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Выдать монеты",
            ),
            disnake.SelectOption(
                label="Изъять монеты",
            ),
            
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="MoneyMenu", min_values=1, max_values=1)
    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0] 
        if selected_option == "Выдать монеты":
            await interaction.response.send_modal(ModalAddMoneyEconomy(self.member)) 
        elif selected_option == "Изъять монеты":
            await interaction.response.send_modal(ModalDellCoinEconomy(self.member)) 

        
        
class RubySelect(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Выдать рубины",
            ),
            disnake.SelectOption(
                label="Изъять рубины",
            ),
            
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="MoneyMenu", min_values=1, max_values=1)
    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Выдать рубины":
           await interaction.response.send_modal(ModalAddRubyEconomy(self.member)) 
        elif selected_option == "Изъять рубины":
           await interaction.response.send_modal(ModalDellRubyEconomy(self.member)) 
        
class ScoreSelect(disnake.ui.Select):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        options = [
            disnake.SelectOption(
                label="Выдать опыт",
            ),
            disnake.SelectOption(
                label="Изъять опыт",
            ),
            
        ]
        super().__init__(placeholder="Выберите функцию...", options=options, custom_id="MoneyMenu", min_values=1, max_values=1)
    
    async def callback(self, interaction: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option == "Выдать опыт":
            await interaction.response.send_modal(ModalAddScoreEconomy(self.member)) 
        elif selected_option == "Изъять опыт":
            await interaction.response.send_modal(ModalDellScoreEconomy(self.member))      
        
            
# ВЫЗОВЫ ВЬЮШЕК
class AdminMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(SelectMenu(member))
        
        
class MuteMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(MuteSelect(member))
        self.add_item(ButtonBack(member))
        

class WarnMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(WarnSelect(member))
        self.add_item(ButtonBack(member))
        
class EconomyMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(EconomySelect(member))
        self.add_item(ButtonBack(member))

class MoneyMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(MoneySelect(member))
        self.add_item(ButtonBackEconomy(member))

class RubyMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(RubySelect(member))
        self.add_item(ButtonBackEconomy(member))
        
class ScoreMenuViews(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.add_item(ScoreSelect(member))
        self.add_item(ButtonBackEconomy(member))



# Кнопка назад     
class ButtonBack(disnake.ui.Button):
    def __init__(self, member: disnake.Member):
        self.member = member
        super().__init__(label="Назад", style=disnake.ButtonStyle.blurple, custom_id="btBack")

    async def callback(self, interaction: disnake.Interaction):
        view = AdminMenuViews(self.member)
        await interaction.response.edit_message(view=view)
        
class ButtonBackEconomy(disnake.ui.Button):
    def __init__(self, member: disnake.Member):
        self.member = member
        super().__init__(label="Назад", style=disnake.ButtonStyle.blurple, custom_id="btBackEconomy")

    async def callback(self, interaction: disnake.Interaction):
        view = EconomyMenuViews(self.member)
        await interaction.response.edit_message(view=view)
        
        
# Модальные окна

class ModalDeleteWarn(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        components = [
            disnake.ui.TextInput(label="Количество предупреждений", placeholder="Введите кол-во предупреждений", custom_id="count_warns"),
        ]

        title = f"Снятие предупреждения у {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalDeleteWarn")
        
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        countDeleteWarn = interaction.text_values["count_warns"]
        
        await userDB.create_table_warns()
        result_cheak_db = await userDB.check_user_warndb(self.member.id)
        
        if result_cheak_db: # Если пользователь есть в таблице тогда
            await userDB.delete_warn_user(self.member.id, countDeleteWarn)
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Снятие предупреждения")
            embed.description = f"### {interaction.author.mention}, вы успешно сняли предупреждение пользователю {self.member.mention} " \
                                f"в количестве {countDeleteWarn}."
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            
            log_channel = await logsDB.get_log_channel(interaction.guild)
            if not log_channel:
                await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
            else:
                channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
                await channel.send(f"### (Снятие предупреждения) Администратор {interaction.author.mention} снял предупреждение пользователю {self.member.mention} в количестве {countDeleteWarn}")
                
        else: # Если лож
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Пользователя не найдено!")
            embed.description = f"### {interaction.author.mention}, Пользователь {self.member.mention} " \
                                f"не найден в таблице."
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        

class ModalWarn(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        components = [
            disnake.ui.TextInput(label="Количество предупреждений", placeholder="Введите количество предупреждений", custom_id="count_warns"),
            disnake.ui.TextInput(label="Причина предупреждения", placeholder="Введите причину предупреждения", custom_id="reason")
        ]

        title = f"Выдача варна - {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalWarn")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        countWarn = interaction.text_values["count_warns"]
        reason = interaction.text_values["reason"]
        
        await userDB.create_table_warns()
        result_cheak_db = await userDB.check_user_warndb(self.member.id)
        
        if result_cheak_db: # Если пользователь есть в таблице тогда
            if await userDB.get_user_warn_count(self.member.id) >= 3: # Проверяем количество предупреждений и кикаем если больше или равно 3
                await self.member.kick()
                await interaction.response.send_message("### Количество предупреждений пользователя было больше 3-х он был изгнан с сервера.", ephemeral=True)
                await userDB.delete_user_from_all_databases(self.member.id)
                
            elif await userDB.get_user_warn_count(self.member.id) < 3: # Если меньше 3 тогда обновляем количество предупреждений
                await userDB.update_warns(interaction, self.member.id, countWarn)
                
                embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Предупреждение выдано!")
                embed.description = f"### {interaction.author.mention}, Вы успешно выдали предупреждение пользователю {self.member.mention} " \
                                    f"в количестве {countWarn}"
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
                log_channel = await logsDB.get_log_channel(interaction.guild)
                
                if not log_channel:
                    await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
                else:
                    channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
                    await channel.send(f"### Администратор {interaction.author.mention} выдал предупреждение пользователю {self.member.mention} в количестве {countWarn} ( по причине: {reason})")
                
                if await userDB.get_user_warn_count(self.member.id) >= 3: # Опять проверяем в случае истины кикаем
                    await self.member.kick()
                    await interaction.response.send_message("Количество предупреждений пользователя было больше 3-х он был изгнан с сервера.")
                    await userDB.delete_user_from_all_databases(self.member.id)
        else: # Если лож
            await userDB.create_table_warns()
            await userDB.insert_warns(interaction, self.member.id, self.member.name, countWarn)
            
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Предупреждение выдано!")
            embed.description = f"### {interaction.author.mention}, Вы успешно выдали предупреждение пользователю {self.member.mention} " \
                                f"в количестве {countWarn}"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            log_channel = await logsDB.get_log_channel(interaction.guild)
            if not log_channel:
                await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
            else:
                channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
                await channel.send(f"### Администратор {interaction.author.mention} выдал предупреждение пользователю {self.member.mention} в количестве {countWarn} ( по причине: {reason})")
                
                
class ModalMute(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Время мута (в минутах)", placeholder="Введите времяя мута",
                                 custom_id="time"),
            disnake.ui.TextInput(label="Причина мута", placeholder="Введите причину мута", custom_id="reason")
        ]

        title = f"Замьют пользователя {member.name}"

        super().__init__(title=title, components=components, custom_id="modalMute")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        time_str = interaction.text_values["time"]
        reason = interaction.text_values["reason"]
        time_minutes = int(time_str)

        time = datetime.datetime.now() + datetime.timedelta(minutes=time_minutes)
        await self.member.timeout(until=time, reason=reason)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Пользователь замючен!")
        embed.description = f"### {interaction.author.mention}, Вы успешно замьютили пользователя {self.member.mention} " \
                            f"на `{time_minutes}` минут"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} замьютил пользователя {self.member.mention} на {time_minutes} ( по причине: {reason})")

            
            
class ModalRename(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        components = [
            disnake.ui.TextInput(label="Новое имя пользователя", placeholder="Введите новое имя пользователя", custom_id="new_name"),
            disnake.ui.TextInput(label="Причина изменения", placeholder="Введите причину изменения", custom_id="reason")
        ]
        
        title = f"Изменение имени пользователя {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalReaname")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        new_name = interaction.text_values["new_name"]
        reason = interaction.text_values["reason"]
        
        await self.member.edit(nick=new_name)        
        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Имя изменино!")
        embed.description = f"### {interaction.author.mention}, Вы успешно изменили имя пользователю {self.member.mention} " \
                            f"на {new_name}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} изменил имя пользователю {self.member.mention} на {new_name} ( по причине: {reason})")


class ModalAddMoneyEconomy(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        
        components = [
            disnake.ui.TextInput(label= f"Количество монет", placeholder=f"Введите количество выдаваемых монет", custom_id="add_value"),
        ]
        
        title = f"Выдача монет {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalAddCoin")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        add_value = interaction.text_values["add_value"]
        
        await rankDB.update_coins(self.member.id, add_value)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Успешно!")
        embed.description = f"### {interaction.author.mention}, Вы успешно выдали пользователю {self.member.mention} монеты в количестве {add_value}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} выдал пользователю {self.member.mention} монеты в количестве {add_value}")
            
class ModalAddRubyEconomy(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        
        components = [
            disnake.ui.TextInput(label= f"Количество рубинов", placeholder=f"Введите количество выдаваемых рубинов", custom_id="add_value"),
        ]
        
        title = f"Выдача рубинов {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalAddRuby")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        add_value = interaction.text_values["add_value"]
        
        await rankDB.update_ruby(self.member.id, add_value)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Успешно!")
        embed.description = f"### {interaction.author.mention}, Вы успешно выдали пользователю {self.member.mention} рубины в количестве {add_value}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} выдал пользователю {self.member.mention} рубины в количестве {add_value}")


class ModalAddScoreEconomy(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        
        components = [
            disnake.ui.TextInput(label= f"Количество опыта", placeholder=f"Введите количество выдаваемого опыта", custom_id="add_value"),
        ]
        
        title = f"Выдача опыта {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalAddScore")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        add_value = interaction.text_values["add_value"]
        
        await rankDB.update_score_admin_panel(self.member.id, add_value)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Успешно!")
        embed.description = f"### {interaction.author.mention}, Вы успешно выдали пользователю {self.member.mention} очки опыта в количестве {add_value}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} выдал пользователю {self.member.mention} очки опыта в количестве {add_value}")


class ModalDellScoreEconomy(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        
        components = [
            disnake.ui.TextInput(label= f"Количество опыта", placeholder=f"Введите количество изымаемого опыта", custom_id="add_value"),
        ]
        
        title = f"Изъятие опыта {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalDellScore")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        add_value = interaction.text_values["add_value"]
        
        await rankDB.update_score_admin_panel_dek(self.member.id, add_value)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Успешно!")
        embed.description = f"### {interaction.author.mention}, Вы успешно изъяли пользователю {self.member.mention} очки опыта в количестве {add_value}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} изъял у пользователя {self.member.mention} очки опыта в количестве {add_value}")


class ModalDellRubyEconomy(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        
        components = [
            disnake.ui.TextInput(label= f"Количество рубинов", placeholder=f"Введите количество изымаемых рубинов", custom_id="add_value"),
        ]
        
        title = f"Изъятие ребинов {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalDellRuby")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        add_value = interaction.text_values["add_value"]
        
        await rankDB.update_ruby_dek(self.member.id, add_value)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Успешно!")
        embed.description = f"### {interaction.author.mention}, Вы успешно изъяли пользователю {self.member.mention} рубины в количестве {add_value}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} изъял у пользователя {self.member.mention} рубины в количестве {add_value}")

class ModalDellCoinEconomy(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        
        components = [
            disnake.ui.TextInput(label= f"Количество монет", placeholder=f"Введите количество изымаемых монет", custom_id="add_value"),
        ]
        
        title = f"Изъятие монет {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalDellCoin")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        add_value = interaction.text_values["add_value"]
        
        await rankDB.update_ruby(self.member.id, add_value)

        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Успешно!")
        embed.description = f"### {interaction.author.mention}, Вы успешно изъяли пользователю {self.member.mention} монеты в количестве {add_value}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_channel = await logsDB.get_log_channel(interaction.guild)
        if not log_channel:
            await interaction.send(f"### В гильдии не установлен канал логирования. Используйте  - `/sel_log`", ephemeral=True)
        else:
            channel = interaction.guild.get_channel(log_channel)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"### Администратор {interaction.author.mention} изъял у пользователя {self.member.mention} монеты в количестве {add_value}")
