import disnake
from disnake.ext import commands
import sqlite3
import asyncio
import datetime
from config import *

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
con = sqlite3.connect('warns.db')
cur = con.cursor()


@bot.event
async def on_ready():
    cur.execute("""CREATE TABLE IF NOT EXISTS warns(
        id INT,
        number INT,
        reason TEXT,
        num INT    
        )
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS cases(
        num INT
        )
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS nums(
        id INT,
        num INT
        )
        """)
    for guild in bot.guilds:     
        for member in guild.members:     
            if cur.execute(     
                    f"SELECT id FROM nums WHERE id = {member.id}").fetchone() is None:     
                cur.execute(f"INSERT INTO nums VALUES ({member.id}, 0)")     
                con.commit() 
    print(bot.user)

@bot.event     
async def on_member_join(member):            
    if cur.execute(     
            f"SELECT id FROM nums WHERE id = {member.id}").fetchone() is None:     
            cur.execute(f"INSERT INTO nums VALUES ({member.id}, 0)")     
            con.commit() 
            msg = disnake.Embed(title="Новый участник)", description=f"<@{member.id}> зашел на сервер!", color=0x00ff00)
    await bot.get_channel(1180985530549284895).send(embed=msg)

@bot.event
async def on_member_remove(member):
    exit_msg = disnake.Embed(title="Нас покинули(", description=f"<@{member.id}> покинул сервер!", color=0xff0000)
    await bot.get_channel(1180985530549284895).send(embed=exit_msg)

@bot.event
async def on_message_edit(before, after):
    msg_msg = disnake.Embed(title="Редактирование", description=f"***Старое сообщение***\n```{before.content}```\n***Новое сообщение***\n```{after.content}```", color=0xffff00)
    await bot.get_channel(1180985530549284895).send(embed=msg_msg)

@bot.event
async def on_message_delete(message):
    msg_del = disnake.Embed(title="Сообщение удалено", description=f"***Удаленное сообщение***\n ```{message.content}```", color=0xff8800)
    await bot.get_channel(1180985530549284895).send(embed=msg_del)

@bot.event
async def on_voice_state_update(member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
    if before.channel is None:
        voice_msg = disnake.Embed(title="Соединение", description=f"{member.display_name} присоеденился к {after.channel.mention}", color=0x0000ff)
        await bot.get_channel(1180985530549284895).send(embed=voice_msg)
    elif after.channel is None:
        voice_msg1 = disnake.Embed(title="Покидение", description=f"{member.display_name} вышел из {before.channel.mention}", color=0x0000ff)
        await bot.get_channel(1180985530549284895).send(embed=voice_msg1)
    elif before.channel != after.channel:
        voice_msg2 = disnake.Embed(title="Переход", description=f"{member.display_name} перешел в {before.channel.mention} из {after.channel.mention}", color=0x0000ff)
        await bot.get_channel(1180985530549284895).send(embed=voice_msg2)

@bot.slash_command(
    options=[
        disnake.Option(
            name="участник",
            description="Выберите участника",
            type=disnake.OptionType.user,
            required=True,
            ),
        disnake.Option(
            name="роль",
            description="Выберите роль",
            type=disnake.OptionType.string,
            required=True,
            choices=[
                disnake.OptionChoice(name="Мальчик", value="m"),
                disnake.OptionChoice(name="Девочка", value="d")
            ]
        )
    ]
)
@commands.has_any_role(1180838814034432081)
async def verify(ctx, участник: disnake.Member, роль: str):
    if роль == 'm':
        await участник.add_roles(disnake.Object(1180851316264808470))
    elif роль == 'd':
        await участник.add_roles(disnake.Object(1180850874759794708))
    await ctx.send(f"Вы успешно верифицировали участника <@{участник.id}>")

@bot.slash_command()
async def action(ctx):
    role = ctx.guild.get_role(1180839139894100008)
    embed = disnake.Embed(
        title="Action Panel",
        description="Для взаимодействия нажмите на кнопки ниже",
        color=0x00ddff
    )

    embed.add_field(name="Мьют/Размьют", value="Осуществляет заглушение или разглушение участника", inline=False)
    embed.add_field(name="Кик", value="Выгоняет участника с сервера", inline=False)
    embed.add_field(name="Бан/Разбан", value="Осуществляет бан или разбан участника", inline=False)
    embed.add_field(name="Выдать/Снять предупреждение", value="Выдает или снимает предупреждение участнику", inline=False)

    row_mute_unmute = disnake.ui.ActionRow(mute_button, unmute_button)
    row_kick_ban_unban = disnake.ui.ActionRow(kick_button, ban_button, unban_button)
    row_warn_unwarn = disnake.ui.ActionRow(warn_button, unwarn_button)

    if role in ctx.author.roles:
        await ctx.send(embed=embed, components=[row_mute_unmute, row_kick_ban_unban, row_warn_unwarn], ephemeral=True)
    else:
        await ctx.send("У вас нет разрешений на использование данной команы.")

@bot.event
async def on_button_click(inter: disnake.Interaction):
    custom_id = inter.component.custom_id
    if custom_id == "mute":
        await inter.response.send_modal(modal=Modal_mute())
    elif custom_id == "unmute":
        await inter.response.send_modal(modal=Modal_unmute())
    elif custom_id == "kick":
        await inter.response.send_modal(modal=Modal_kick())
    elif custom_id == "ban":
        await inter.response.send_modal(modal=Modal_ban())
    elif custom_id == "unban":
        await inter.response.send_modal(modal=Modal_unban())
    elif custom_id == "warn":
        await inter.response.send_modal(modal=Modal_warn())
    elif custom_id == "unwarn":
        await inter.response.send_modal(modal=Modal_unwarn())

bot.run(token)
