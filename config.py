import disnake
from disnake.ext import commands
import datetime
import asyncio
import sqlite3

token = "MTE4Mjc0NjQ3MDQwODAxNTk2Mw.GTKDjo.KTQzY8hYdfJUFll3nyzSpZLmGvi6aIJ6M0Xga0"
con = sqlite3.connect('warns.db')
cur = con.cursor()
mute_button = disnake.ui.Button(style=disnake.ButtonStyle.green, label="Мьют", custom_id="mute")
unmute_button = disnake.ui.Button(style=disnake.ButtonStyle.green, label="Размьют", custom_id="unmute")
kick_button = disnake.ui.Button(style=disnake.ButtonStyle.red, label="Кик", custom_id="kick")
ban_button = disnake.ui.Button(style=disnake.ButtonStyle.red, label="Бан", custom_id="ban")
unban_button = disnake.ui.Button(style=disnake.ButtonStyle.red, label="Разбан", custom_id="unban")
warn_button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Выдать предупреждение", custom_id="warn")
unwarn_button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Снять предупреждение", custom_id="unwarn")

def parse_time(time_str):
    unit = time_str[-1].lower()
    time_value = int(time_str[:-1])

    if unit == 's':
        return time_value
    elif unit == 'm':
        return time_value * 60
    elif unit == 'h':
        return time_value * 60 * 60
    elif unit == 'с':
        return time_value
    elif unit == 'м':
        return time_value * 60
    elif unit == 'ч':
        return time_value * 60 * 60
    elif unit == 'd':
        return time_value * 60 * 60 * 24
    elif unit == 'д':
        return time_value * 60 * 60 * 24
    else:
        raise commands.BadArgument("Invalid time unit. Use 's' for seconds, 'm' for minutes, or 'h' for hours.")

class Modal_mute(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Айди пользователя",
                placeholder="Введите айди пользователя",
                custom_id="mute_id",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Длительность",
                placeholder="Введите длительность мьюта",
                custom_id="duration",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Причина",
                placeholder="Введите причину мьюта",
                custom_id="reason",
                style=disnake.TextInputStyle.short,
            )
        ]
        super().__init__(
            title="Мьют",
            custom_id="mute",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        id = int(inter.text_values["mute_id"])
        dur = str(inter.text_values["duration"])
        reas = (inter.text_values["reason"])
        duration_seconds = parse_time(dur)
        until_time = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
        member = inter.guild.get_member(id)

        await member.timeout(reason=reas, until=until_time)
        await inter.response.send_message(f"Участник {member.mention} был замьючен на {dur}, по причине - {reas}")
        await member.send(f"Вы были замьючены на сервере EDEM на {dur}, по причине {reas}")

class Modal_unmute(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Айди пользователя",
                placeholder="Введите айди пользователя",
                custom_id="unmute_id",
                style=disnake.TextInputStyle.short)
            ]
        super().__init__(
            title="Размьют",
            custom_id="unmute",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        id = int(inter.text_values["unmute_id"])
        member = inter.guild.get_member(id)
        until_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
        await member.timeout(until=until_time)
        await inter.response.send_message(f"Участник {member.mention} был размьючен")

class Modal_kick(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Айди пользователя",
                placeholder="Введите айди пользователя",
                custom_id="kick_id",
                style=disnake.TextInputStyle.short)
            ]
        super().__init__(
            title="Кик",
            custom_id="kick",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        id = int(inter.text_values["kick_id"])
        member = inter.guild.get_member(id)
        await member.send("Вы были выгнаны с сервера EDEM")
        await member.kick()
        await inter.response.send_message(f"Участник {member.mention} был выгнан")

class Modal_ban(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Айди пользователя",
                placeholder="Введите айди пользователя",
                custom_id="ban_id",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Длительность",
                placeholder="Введите длительность бана",
                custom_id="duration",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Причина",
                placeholder="Введите причину бана",
                custom_id="reason",
                style=disnake.TextInputStyle.short,
            )
        ]
        super().__init__(
            title="Бан",
            custom_id="ban",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        id = int(inter.text_values["ban_id"])
        dur = str(inter.text_values["duration"])
        reas = (inter.text_values["reason"])
        duration_seconds = parse_time(dur)
        member = inter.guild.get_member(id)
        member_id = member.id


        await inter.response.send_message(f'{member.mention} забанен на {dur}, по причине {reas}')
        await member.send(f'Вы были забанены на сервере {inter.guild.name} на {dur}, по причине {reas}')
        await member.ban(reason=reas)

        await asyncio.sleep(duration_seconds)
        ban_entry = await inter.guild.fetch_ban(disnake.Object(member_id))
        # Разбан пользователя
        await inter.guild.unban(ban_entry.user)
        link = await inter.channel.create_invite(max_age=300)
        await ban_entry.user.send(f'У вас закончился бан на сервере "{inter.guild.name}"! {link}')

class Modal_unban(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Айди пользователя",
                placeholder="Введите айди пользователя",
                custom_id="unban_id",
                style=disnake.TextInputStyle.short)
            ]
        super().__init__(
            title="Разбан",
            custom_id="unban",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        id = int(inter.text_values["unban_id"])
        ban_entry = await inter.guild.fetch_ban(disnake.Object(id))
        await inter.guild.unban(ban_entry.user)
        link = await inter.channel.create_invite(max_age=300)
        await ban_entry.user.send(f'У вас закончился бан на сервере "{inter.guild.name}"! {link}')
        await inter.response.send_message(f'<@{id}> был разбанен')

class Modal_warn(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Айди пользователя",
                placeholder="Введите айди пользователя",
                custom_id="warn_id",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Длительность",
                placeholder="Введите длительность предупреждения",
                custom_id="duration",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Причина",
                placeholder="Введите причину предупреждения",
                custom_id="reason",
                style=disnake.TextInputStyle.short,
            )
        ]
        super().__init__(
            title="Предупреждение",
            custom_id="warn",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        id = int(inter.text_values["warn_id"])
        dur = str(inter.text_values["duration"])
        reas = (inter.text_values["reason"])
        duration_seconds = parse_time(dur)
        member = inter.guild.get_member(id)

        duration_seconds = parse_time(dur)
        num = cur.execute(f"SELECT num FROM cases").fetchone()[0]
        number = cur.execute(f"SELECT num FROM nums WHERE id = {member.id}").fetchone()[0]
        number1 = num + 1
        cur.execute(f"INSERT INTO warns VALUES ({member.id}, {number1}, '{reas}', {num + 1})")
        cur.execute(f"UPDATE nums SET num = num + 1 WHERE id = {member.id}")
        cur.execute(f"UPDATE cases SET num = num + 1")
        con.commit()
        await inter.response.send_message(f"Вы успешно выдали предупрездение участнику <@{member.id}>, на {dur}, по причине {reas}")
        await member.send(f"Вы получили предупрездение на {dur}, по причине {reas}")
        await asyncio.sleep(duration_seconds)
        cur.execute(f"DELETE FROM warns WHERE num = {number1}")
        cur.execute(f"UPDATE nums SET num = num - 1 WHERE id = {member.id}")
        con.commit()
        
class Modal_unwarn(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Случай",
                placeholder="Введите случай предупреждения",
                custom_id="case",
                style=disnake.TextInputStyle.short,
            )
        ]
        super().__init__(
            title="Снять предупреждение",
            custom_id="unwarn",
            components=components,
        )
    
    async def callback(self, inter:disnake.Interaction):
        case = str(inter.text_values["case"])

        member = cur.execute(f"SELECT id FROM warns WHERE num = {case}").fetchone()[0]
        cur.execute(f"DELETE FROM warns WHERE num = {case}")
        cur.execute(f"UPDATE nums SET num = num - 1 WHERE id = {member}")
        await inter.response.send_message(f"Вы успешно сняли предупрждение {case}")
        con.commit()
