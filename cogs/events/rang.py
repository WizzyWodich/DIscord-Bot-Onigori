import disnake, datetime
from disnake.ext import commands
from database.RankDatabase import RankDatabase


class RankingEvents(commands.Cog):
    def __init__(self, bot):
        self.START_DATE = datetime.date(2024, 9, 1)
        self.END_DATE = datetime.date(2024, 9, 30)
        self.CURRENCY_AMOUNT = 3  
        self.bot = bot
        self.rank_db = RankDatabase()
        self.voice_start_times = {}


    async def check_event_period(self):
        today = datetime.date.today()
        return self.START_DATE <= today <= self.END_DATE

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, disnake.DMChannel):
            return
        if len(message.content) == 1:
            return

        await self.rank_db.add_user(message.author)
        level_up_result = await self.rank_db.update_level_method(message.author.id)

        if level_up_result:
            try:
                user = await self.bot.fetch_user(message.author.id)
                user_level = await self.rank_db.get_user_level(message.author.id)
                await user.send(f"### Ваш уровень повысился до {user_level}. Поздравляем!")
                print(f"Сообщение отправлено пользователю {message.author.id}")  # Логирование отправки сообщения
            except disnake.Forbidden:
                print(f"Не удалось отправить сообщение пользователю {message.author.id}")  # Логирование ошибки

        score_update_result = await self.rank_db.update_score(message.author.id)

        coins = await self.rank_db.get_user_coins(message.author.id)
        rubins = await self.rank_db.get_user_rubins(message.author.id)
        score = await self.rank_db.get_user_score(message.author.id)

        await self.rank_db.update_message_count(message.author.id)

        rank_coins = await self.rank_db.get_user_rank_by_coins(message.author.id)
        rank_rubins = await self.rank_db.get_user_rank_by_rubins(message.author.id)
        rank_score = await self.rank_db.get_user_rank_by_score(message.author.id)

        if await self.check_event_period():
            if len(message.content) == 2:
                print("Длина содержимого сообщения 2. Специальная обработка события.")
                return  

            message_count = await self.rank_db.get_user_message_count(message.author.id)
            message_count += 1

            if message_count % 5 == 0:
                await self.rank_db.update_ivent_coins(message.author.id, self.CURRENCY_AMOUNT)
            
        if await self.check_event_period():
            if len(message.content) == 2:
                return  
            
            message_count = await self.rank_db.get_user_message_count(message.author.id)
            message_count += 1

            if message_count % 5 == 0:
                await self.rank_db.update_ivent_coins(message.author.id, self.CURRENCY_AMOUNT)
            
            await self.rank_db.update_message_count(message.author.id, message_count)
        else:
            print('Событие еще не началось или уже закончилось.') 

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            self.voice_start_times[member.id] = disnake.utils.utcnow()
        elif before.channel is not None and after.channel is None:
            if member.id in self.voice_start_times:
                voice_time = disnake.utils.utcnow() - self.voice_start_times[member.id]
                minutes = int(voice_time.total_seconds() // 60)
                await self.rank_db.update_voice_time(member.id, minutes)
                del self.voice_start_times[member.id]
                
def setup(bot):
    bot.add_cog(RankingEvents(bot))