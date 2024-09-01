import aiohttp, io, disnake, random, datetime


from PIL import Image, ImageFont, ImageDraw
from disnake.ext import commands
from database.RankDatabase import RankDatabase


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rank_db = RankDatabase()
        self.voice_start_times = {}
        self.bot_owner_id = 914812102768734258
    
    async def get_avatar(self, url: str) -> bytes: # алгоритм жля получения и чтения аватара юзера
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar = await resp.read()
        return avatar

    async def limit_string_length(self, string, max_length=15) -> None: # сокращение никнейма
        if len(string) > max_length:
            return f'{string[:max_length-1]}...'
        else:
            return string
    
    @commands.slash_command(description='Информация о профиле')
    async def profile(self, interaction: disnake.AppCommandInteraction, member: disnake.Member = commands.Param(default=lambda m: m.author, description='Пользователь')):
        await interaction.response.defer()

        achievements = {
            "bot_owner": "image/achievements/owner_bot.png",
            "server_owner": "image/achievements/owner_server.png",
            "member": "image/achievements/member.png",
            "10lvl": "image/achievements/10lvl.png",
            "25lvl": "image/achievements/25lvl.png",
            "50lvl": "image/achievements/50lvl.png",
            "100lvl": "image/achievements/100lvl.png",
            "Toplvl": "image/achievements/Top10Score.png"
        }
        
        if member.id == interaction.guild.owner_id and member.id == self.bot_owner_id:
            achievement_key = "bot_owner"
        elif member.id == interaction.guild.owner_id:
            achievement_key = "server_owner"
        elif member.id == self.bot_owner_id:
            achievement_key = "bot_owner"
        else:
            achievement_key = "member"

        # Загрузка изображения достижения
        achievement_image = Image.open(achievements[achievement_key]).convert("RGBA")
        
        # Получение данных из базы данных
        level = await self.rank_db.get_user_level(member.id)
        score = await self.rank_db.get_user_score(member.id)
        new_score = await self.rank_db.get_user_new_score(member.id)
        coins = await self.rank_db.get_user_coins(member.id)
        rubins = await self.rank_db.get_user_rubins(member.id)
        top_coins = await self.rank_db.get_user_rank_by_coins(member.id)
        top_ruby = await self.rank_db.get_user_rank_by_rubins(member.id)
        top_score = await self.rank_db.get_user_rank_by_score(member.id)
        top_messages = await self.rank_db.get_user_rank_by_messages(member.id)
        top_voice = await self.rank_db.get_user_rank_by_voice_time(member.id)
        
        # Ivent
        countСhestnut = await self.rank_db.get_user_ivent_coins(member.id)
        
         # Выбор изображений для достижений
        perck_level_image = None
        if level >= 100:
            perck_level_image = Image.open(achievements["100lvl"]).convert("RGBA")
        elif level >= 50:
            perck_level_image = Image.open(achievements["50lvl"]).convert("RGBA")
        elif level >= 25:
            perck_level_image = Image.open(achievements["25lvl"]).convert("RGBA")
        elif level >= 10:
            perck_level_image = Image.open(achievements["10lvl"]).convert("RGBA")
        
        percks_top_images = None
        if top_score <= 10:
            percks_top_images = Image.open(achievements["Toplvl"]).convert("RGBA")
        
        # Фон и шрифты
        status_images = {
            disnake.Status.online: ('image/rang/UserOnline.png', '#40CC33'),
            disnake.Status.idle: ('image/rang/UserINL.png', '#FFA90A'),
            disnake.Status.dnd: ('image/rang/UserDND.png', '#F6361D'),
            disnake.Status.offline: ('image/rang/UserOffline.png', '#434343')
        }
        
        background_path, color_bar = status_images.get(member.status, status_images[disnake.Status.offline])
        background = Image.open(background_path)
        fill_color = "#FFFFFF"  # Белый цвет
        fill_color_lvl = '#353535'
        
        backdraw = ImageDraw.Draw(background)
        font = ImageFont.truetype('font/IBMPlexSerif-Medium.ttf', size=48)
        font_name = ImageFont.truetype('font/IBMPlexSerif-Medium.ttf', size=24)
        font_top_lvl = ImageFont.truetype('font/IBMPlexSerif-Medium.ttf', size=32)
        font_lvl = ImageFont.truetype('font/IBMPlexSerif-Medium.ttf', size=48)
        font_progress = ImageFont.truetype('font/IBMPlexSerif-Medium.ttf', size=18)

        # Аватарка
        avatar = await self.get_avatar(member.display_avatar.url)
        avatar_image = Image.open(io.BytesIO(avatar))
        avatar_image = avatar_image.resize((300, 300), Image.LANCZOS)
        bigsize = (avatar_image.size[0] * 3, avatar_image.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, 255)
        mask = mask.resize(avatar_image.size, Image.LANCZOS)
        background.paste(avatar_image, (804, 102), mask)
        
        background.paste(achievement_image, (795, 86), achievement_image)
        
        if perck_level_image:
            background.paste(perck_level_image, (173, 525), perck_level_image)

        if percks_top_images:
            background.paste(percks_top_images, (75, 525), percks_top_images)
            
        # Display name
        name = await self.limit_string_length(member.display_name)
        text_width = backdraw.textbbox((0, 0), name, font=font)[2] - backdraw.textbbox((0, 0), name, font=font_name)[0]
        x = (562 - text_width) // 2 + 1313
        backdraw.text((x, 123), name, font=font_name, fill=fill_color)

        # Progress Bar
        bar_offset_x = 69
        bar_offset_y = 630 
        bar_offset_x_1 = 1833
        bar_offset_y_1 = 687
        circle_size = bar_offset_y_1 - bar_offset_y
        bar_length = bar_offset_x_1 - bar_offset_x
        req = new_score
        xp = score
        
        progress = (req - xp) * 100 / req
        progress = 100 - progress
        progress_bar_length = round(bar_length * progress / 100)
        bar_offset_x_1 = bar_offset_x + progress_bar_length

        backdraw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill=color_bar)
        backdraw.ellipse((bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill=color_bar)
        backdraw.ellipse((bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill=color_bar)

        # Progress text
        progress_text = f'{int(progress)}%'
        text_width = backdraw.textlength(progress_text, font)
        x = (72 - text_width) // 2 + 1095
        backdraw.text((x, 547), progress_text, font=font_progress, fill=fill_color_lvl)

        # Experience/Level text
        if req >= 10000:
            req = f'{str(req)[:-3]}k'
        if xp >= 10000:
            xp = f'{str(xp)[:-3]}k'
        if countСhestnut >= 1000:
            countСhestnut = f'{str(countСhestnut)[:-3]}k'

        rank = f'{xp}/{req}'
        text_width = backdraw.textlength(rank, font)
        x = (398 - text_width) // 2 + 1321
        backdraw.text((x, 488), rank, font=font, fill=fill_color)

        # Top rank
        top = str(top_score)
        text_width = backdraw.textlength(top, font)
        x = (88 - text_width) // 2 + 764
        backdraw.text((x, 533), top, font=font_top_lvl, fill=fill_color_lvl)


        # Ivent
        ivent = str(countСhestnut)
        text_width = backdraw.textlength(ivent, font)
        x = (88 - text_width) // 2 + 628
        backdraw.text((x, 533), ivent, font=font_top_lvl, fill=fill_color_lvl)


        # Level text
        lvl = str(level)
        text_width = backdraw.textlength(lvl, font=font)
        x = (133 - text_width) // 2 + 892
        backdraw.text((x, 490), lvl, font=font_lvl, fill=fill_color_lvl)

        # Правае крыло
        coin = str(coins)
        text_width = backdraw.textlength(coin, font)
        x = (344 - text_width) // 2 + 207
        backdraw.text((x, 157), coin, font=font, fill=fill_color)

        rubin = str(rubins)
        text_width = backdraw.textlength(rubin, font)
        x = (344 - text_width) // 2 + 207
        backdraw.text((x, 323), rubin, font=font, fill=fill_color)

        # Левое крыло

        top_rubins = str(top_ruby)
        text_width = backdraw.textlength(top_rubins, font)
        x = (198 - text_width) // 2 + 1321
        backdraw.text((x, 333), top_rubins, font=font, fill=fill_color)

        top_coin = str(top_coins)
        text_width = backdraw.textlength(top_coin, font)
        x = (198 - text_width) // 2 + 1321
        backdraw.text((x, 252), top_coin, font=font, fill=fill_color)

        top_msg = str(top_messages)
        text_width = backdraw.textlength(top_msg, font)
        x = (198 - text_width) // 2 + 1634
        backdraw.text((x, 252), top_msg, font=font, fill=fill_color)

        top_voices = str(top_voice)
        text_width = backdraw.textlength(top_voices, font)
        x = (198 - text_width) // 2 + 1634
        backdraw.text((x, 333), top_voices, font=font, fill=fill_color)

        img_bytes = io.BytesIO()
        background.save(img_bytes, 'PNG')
        img_bytes.seek(0)
        image_file = disnake.File(img_bytes, filename=f'{member.display_name}_profile.png')
        await interaction.followup.send(file=image_file)

def setup(bot):
    bot.add_cog(Profile(bot))
