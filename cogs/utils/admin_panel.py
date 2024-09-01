import disnake
from disnake.ext import commands
import aiohttp, io, disnake, random

from PIL import Image, ImageFont, ImageDraw
from disnake.ui.action_row import ModalUIComponent
from disnake.utils import MISSING
from database.UserInfoDatabase import UsersDataBase
from database.LogsDatabase import LogsDatabase
from database.RankDatabase import RankDatabase

from support import AdminMenuViews

log_db = LogsDatabase()
user_db = UsersDataBase()            
    
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_avatar(self, url: str) -> bytes: # алгоритм жля получения и чтения аватара юзера
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar = await resp.read()
        return avatar

    async def limit_string_length(self, string, max_length=12) -> None: # сокращение никнейма
        if len(string) > max_length:
            return f'{string[:max_length-1]}...'
        else:
            return string

    @commands.slash_command(name="user", description="Управление пользователем", dm_permission=False)
    @commands.has_permissions(administrator=True)
    async def user_panel(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        self.db = RankDatabase()
        view = AdminMenuViews(member)
        
        user_name = member.display_name
        role = max(member.roles, key=lambda role: role.position)
        role_name = role.name  
        countWarnsUser = await user_db.get_user_warn_count(member.id)
        coins = await self.db.get_user_coins(member.id)
        ruby = await self.db.get_user_rubins(member.id)
        score = await self.db.get_user_score(member.id)
        
        await interaction.response.defer(ephemeral=True)
        
        font = ImageFont.truetype('font/IBMPlexSerif-Medium.ttf', 24) # ваш путь к шрифту
        fill_color = '#FFFFFF'
        
        background = Image.open('image/admin_patel/Adminpanel.png') # ваш путь к фону профиля
        backdraw = ImageDraw.Draw(background)   


        avatar = await self.get_avatar(member.display_avatar.url)
        avatar_image = Image.open(io.BytesIO(avatar))
        avatar_image = avatar_image.resize((160, 160), Image.LANCZOS)
        bigsize = (avatar_image.size[0] * 3, avatar_image.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, 255)
        mask = mask.resize(avatar_image.size, Image.LANCZOS)
        background.paste(avatar_image, (26, 21), mask)
        
        name = await self.limit_string_length(user_name)
        text_width = backdraw.textbbox((0, 0), name, font=font)[2] - backdraw.textbbox((0, 0), name, font=font)[0]
        x = (241 - text_width) // 2 + 251
        backdraw.text((x, 50), name, font=font, fill=fill_color)
        
        role_display = await self.limit_string_length(role_name)  # Используем имя роли
        text_width = backdraw.textbbox((0, 0), role_display, font=font)[2] - backdraw.textbbox((0, 0), role_display, font=font)[0]
        x = (176 - text_width) // 2 + 273
        backdraw.text((x, 135), role_display, font=font, fill=fill_color)
        
        if countWarnsUser is None: countWarnsUser = 0
        warns = f'{str(countWarnsUser)}/3'
        text_width = backdraw.textlength(warns, font)
        x = (44 - text_width) // 2 + 335
        backdraw.text((x, 220), warns, font=font, fill=fill_color)
        
        
        if score >= 100000: 
            score = f'{str(score)[:-3]}k' # сокращение чисел
        if coins >= 100000:
            coins = f'{str(coins)[:-3]}k' # сокращение 
        if ruby >= 100000:
            ruby = f'{str(ruby)[:-3]}k' # сокращение
        
        score = str(score)
        text_width = backdraw.textlength(score, font)
        x = (183 - text_width) // 2 + 562
        backdraw.text((x, 219), score, font=font, fill=fill_color)
        
        coins = str(coins)
        text_width = backdraw.textlength(coins, font)
        x = (105 - text_width) // 2 + 615
        backdraw.text((x, 60), coins, font=font, fill=fill_color)
        
        ruby = str(ruby)
        text_width = backdraw.textlength(ruby, font)
        x = (105 - text_width) // 2 + 615
        backdraw.text((x, 128), ruby, font=font, fill=fill_color)
        
        img_bytes = io.BytesIO()
        background.save(img_bytes, 'PNG')
        img_bytes.seek(0)
        image_file = disnake.File(img_bytes, filename=f'{member.display_name}_profile.png')

        await interaction.edit_original_message(view=view, file=image_file)


def setup(bot):
    bot.add_cog(Admin(bot))