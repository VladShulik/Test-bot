import os
import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------ Helpers ------
def server_info_embed(guild: discord.Guild) -> discord.Embed:
    e = discord.Embed(
        title=f"Информация о сервере: {guild.name}",
        color=discord.Color.blurple(),
        timestamp=datetime.datetime.utcnow()
    )
    e.add_field(name="ID", value=guild.id, inline=True)
    e.add_field(name="Участников", value=guild.member_count, inline=True)
    e.add_field(name="Создан", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    if guild.owner:
        e.add_field(name="Владелец", value=f"{guild.owner} ({guild.owner.id})", inline=False)
    if guild.icon:
        e.set_thumbnail(url=guild.icon.url)
    return e

RULES_TEXT = (
    "Правила сервера:\n"
    "1) Уважайте друг друга.\n"
    "2) Без спама и рекламы без разрешения.\n"
    "3) Соблюдайте правила Discord ToS.\n"
    "Если есть вопросы — пишите модераторам."
)

# ------ Events ------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id: {bot.user.id})")
    if LOG_CHANNEL_ID == 0:
        print("⚠️  LOG_CHANNEL_ID не задан — лог удалений работать не будет.")

@bot.event
async def on_message(message: discord.Message):
    # игнорим свои сообщения
    if message.author == bot.user:
        return

    # реакция на слово "привет" (без учёта регистра, ищем как отдельное слово)
    content_lower = message.content.lower()
    # простая проверка: слово 'привет' как есть или окружено пробелами/знаками
    if "привет" in content_lower.split() or "привет" in content_lower.strip(" !?,.;:()[]{}\"'"):
        try:
            await message.channel.send(f"Привет, {message.author.mention}!")
        except discord.Forbidden:
            pass  # нет прав написать — пропускаем

    # не забудь пробросить к командным хендлерам
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message: discord.Message):
    # игнорим системные/пустые случаи
    if message.guild is None:
        return
    if not LOG_CHANNEL_ID:
        return
    if message.author.bot:
        return  # если хочешь логировать ботов — убери эту строку

    channel = bot.get_channel(LOG_CHANNEL_ID)
    if not isinstance(channel, discord.TextChannel):
        return

    embed = discord.Embed(
        title="🗑️ Сообщение удалено",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Автор", value=f"{message.author} ({message.author.id})", inline=False)
    embed.add_field(name="Канал", value=f"{message.channel.mention}", inline=False)
    content = message.content if message.content else "*без текста*"
    # ограничим длину, чтобы embed не взорвался
    if len(content) > 1000:
        content = content[:1000] + " …"
    embed.add_field(name="Содержимое", value=content, inline=False)

    # вложения
    if message.attachments:
        urls = "\n".join(a.url for a in message.attachments[:5])
        embed.add_field(name="Вложения", value=urls, inline=False)

    await channel.send(embed=embed)

# ------ Commands ------
@bot.command(name="info")
async def info(ctx: commands.Context):
    """!info — инфа о сервере"""
    if ctx.guild is None:
        return await ctx.reply("Команда доступна только на сервере.")
    await ctx.send(embed=server_info_embed(ctx.guild))

@bot.command(name="rules")
async def rules(ctx: commands.Context):
    """!rules — отправляет правила в ЛС"""
    try:
        await ctx.author.send(RULES_TEXT)
        await ctx.reply("Отправил правила тебе в ЛС ✅", mention_author=False)
    except discord.Forbidden:
        await ctx.reply("Не могу отправить ЛС (возможно, закрыты личные сообщения).", mention_author=False)

# ------ Run ------
if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN не найден в .env")
    bot.run(TOKEN)
