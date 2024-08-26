import aiosqlite
import disnake
from disnake.ext import commands

class LogsDatabase:
    def __init__(self):
        self.botDatabase = "database/fileDB/BotDDatabase.db"
    
    async def create_table_log_chanel(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS logsChanel (
                                        guildID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        channelLogsID INTEGER NULL
                                    )''')
                await db.commit()
            
    async def insert_logs_channel(self, channel: disnake.TextChannel, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_select = "SELECT * FROM logsChanel WHERE guildID = ?"
                query_insert = "INSERT INTO logsChanel (guildID, channelLogsID) VALUES (?, ?)"
                query_update = "UPDATE logsChanel SET channelLogsID = ? WHERE guildID = ?"

                await cursor.execute(query_select, (guild.id,))
                result = await cursor.fetchone()
                if result:
                    await cursor.execute(query_update, (channel.id, guild.id))
                else:
                    await cursor.execute(query_insert, (guild.id, channel.id))
                await db.commit()
                
    async def get_log_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_check = '''SELECT channelLogsID FROM logsChanel WHERE guildID = ?'''
                await cursor.execute(query_check, (guild.id,))
                channelLogsID = await cursor.fetchone()
                return channelLogsID[0] if channelLogsID else print("В гильдии не установлен канал логирования.")
            
    async def remove_log_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM logsChanel WHERE guildId = ?', (guild.id,))
                await db.commit()