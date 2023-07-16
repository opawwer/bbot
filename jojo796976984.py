import os
import disnake
from disnake.ext import commands, tasks
from discord.ext.commands import BucketType
import random
import sqlite3
import datetime
from datetime import timedelta
import asyncio
from dotenv import load_dotenv
import uuid

load_dotenv
bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
connection = sqlite3.connect('jojo.db')
cursor = connection.cursor()

@bot.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    rp TEXT,
    id INT,
    age INT,
    org TEXT,
    power INT,
    speed INT,
    reaction INT,
    endurance INT,
    sword INT,
    prof INT
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS lvl (
    id INT,
    lvl BIGINT
    )""")

    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', 'отсуствует', {member.id}, 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует')")
                connection.commit()
    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM lvl WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO lvl VALUES ('{member.id}', 0)")
                connection.commit()
    print(f"{bot.user} connected!")

@bot.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', 'отсуствует', {member.id}, 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует', 'отсуствует')")
        connection.commit()
    else:
        pass
    
    if cursor.execute(f"SELECT id FROM lvl WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO lvl VALUES ('{member.id}', 0)")
        connection.commit()
    else:
        pass

@bot.command()
async def инфо(ctx, member: disnake.Member=None):
    if member is None:
        cursor.execute(f"SELECT age, org, power, speed, rp, reaction, endurance, sword, prof FROM users WHERE id = {ctx.author.id}")
        result = cursor.fetchone()
        if result is not None:
            age = result[0]
            org = result[1]
            power = result[2]
            speed = result[3]
            rp = result[4]
            reaction = result[5]
            endurance = result[6]
            sword = result[7]
            prof = result[8]

            embed = disnake.Embed(title=f"Информация о пользователе - {ctx.author}", description=f"**Данные**\nимя персонажа: {rp} \nвозраст: {age}\nорганизация: {org}\nㅤ\n**Статистика**\nсила: {power}\nскорость: {speed}\nреакция: {reaction}\nвыносливость: {endurance}\nвладение мечом: {sword}\nвладение профессией: {prof}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Нет информации о пользователе.")
    
    else:
        cursor.execute(f"SELECT age, org, power, speed, rp, reaction, endurance, sword, prof FROM users WHERE id = {member.id}")
        result = cursor.fetchone()
        if result is not None:
            age = result[0]
            org = result[1]
            power = result[2]
            speed = result[3]
            rp = result[4]
            reaction = result[5]
            endurance = result[6]
            sword = result[7]
            prof = result[8]

            embed = disnake.Embed(title=f"Информация о пользователе - {member}", description=f"**Данные**\nимя персонажа: {rp} \nвозраст: {age}\nорганизация: {org}\nㅤ\n**Статистика**\nсила: {power}\nскорость: {speed}\nреакция: {reaction}\nвыносливость: {endurance}\nвладение мечом: {sword}\nвладение профессией: {prof}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Нет информации о пользователе.")

@bot.command()
@commands.has_permissions(administrator=True)
@commands.has_any_role("1128668840411275394")
async def инфо_сменить(ctx, member: disnake.Member, type: str, *, any: str):
    if type == "имя":
        cursor.execute("UPDATE users SET rp = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Имя персонажа для пользователя {member} успешно обновлено.")
    elif type == "возраст":
        cursor.execute("UPDATE users SET age = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Возраст для пользователя {member} успешно обновлено.")
    elif type == "организация":
        cursor.execute("UPDATE users SET org = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Организация для пользователя {member} успешно обновлено.")
    elif type == "сила":
        cursor.execute("UPDATE users SET power = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Сила для пользователя {member} успешно обновлено.")
    elif type == "скорость":
        cursor.execute("UPDATE users SET speed = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"скорость для пользователя {member} успешно обновлено.")
    elif type == "реакция":
        cursor.execute("UPDATE users SET reaction = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Реакция для пользователя {member} успешно обновлено.")
    elif type == "выносливость":
        cursor.execute("UPDATE users SET endurance = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Выносливость для пользователя {member} успешно обновлено.")
    elif type == "мечь":
        cursor.execute("UPDATE users SET sword = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Владение мечом для пользователя {member} успешно обновлено.")
    elif type == "профессия":
        cursor.execute("UPDATE users SET prof = ? WHERE id = ?", (any, member.id))
        connection.commit()
        await ctx.send(f"Владение профессией для пользователя {member} успешно обновлено.")
    else:
        await ctx.send(f"Указанный пинкт не найден")

@bot.command()
async def фрукт(ctx):
    fruits = ['Arms Fruit', 'Art Fruit', 'Барьер-фрукт', 'Ягода', 'Bis Fruit', 'Плод Боинг', 'Книжный фрукт', 'Плоды Бум, Brain Fruit', 'Кисть-фрукт', 'Bubble Fruit', 'Castle Fruit', 'Clear Fruit', 'Chop Fruit', 'клон-фрукт', 'Cook Fruit', 'Cream Fruit', 'Dice Fruit', 'Дверной фрукт', 'Float Fruit', 'Цветок-Фрукт', 'Garb Fruit', 'Glare Fruit', 'Heal Fruit', 'Jacket Fruit', 'Magnet Fruit', 'Memo Fruit', 'Millet Fruit', 'Munch Fruit', 'Paw Fruit', 'Pop Fruit', 'Pocket Fruit', 'Puff Fruit',  'Push Fruit', 'Revive Fruit', 'Ripple Fruit', 'Rust Fruit', 'Scroll Fruit', 'Shadow Fruit', 'Sick Fruit', 'Slow Fruit', 'Smooth Fruit', 'Snip Fruit', 'Stick Fruit', 'String Fruit', 'TonFruit', 'Diggy Fruit Model Mol', 'Dog Fruit Model Dachsund', 'Dog Fruit Model Jackal', 'Snake Fruit Model Анаконда', 'Snake Fruit Model King Cobra', 'Dark Fruit', 'Flame Fruit', 'Ice Fruit', 'Sand Fruit', 'Swamp Fruit', 'Woods Fruit', 'Clank Fruit', 'Chain Fruit', 'Cube Fruit', 'Gold Fruit', 'Grow Fruit', 'Hard Fruit', 'Lucky Fruit', 'Mini Fruit', 'Net Fruit', 'Pet Fruit', 'Roll Fruit', 'Scream Fruit', 'Sickle Fruit', 'Sleep Fruit', 'Song Fruit', 'Vision Fruit', 'Liquid Fruit', 'Paper Fruit', 'полый фрукт', 'гормовый фрукт', 'Зеркальный фрукт', 'спелый фрукт', 'Мерцающий фрукт', 'Веном', 'Деформация', 'Воск', 'Птица-Птица', 'Конский фрукт', 'Глинт', 'Дым', 'цветной фрукт', 'Гриб-Фрукт']
    result = random.choice(fruits)
    await ctx.reply(f"Поздравляю!\nВам выпало {result}")


timers = {}
islands = ['🌵острова-кактусов🌵', '🌴виски-пик🌴', '🦢остров-драм🦢', '🎓бигхорн🎓', '🌞алабаста🌞', '🌏джая🌏', '☁скайпия☁', '💧water-7💧', '🦁эниес-лобби🦁', '🍴архипелаг-сабаоди🍴', '🕍маринфорд🕍', '🐟остров-рыболюдей🐟', '🧿g-8🧿', '₊✧˚🌊море🌊₊✧˚']

@bot.command()
async def лог_пос(ctx):
    timer_id = str(uuid.uuid4())
    rand_seconds = random.randint(30*60, 24*60*60)
    timers[timer_id] = rand_seconds
    asyncio.create_task(countdown_task(timer_id, ctx.channel.id))
    await ctx.reply(f"лог пос будет настраиваться {rand_seconds // 60 // 60} часов.")

async def countdown_task(timer_id, channel_id):
    while timers[timer_id] > 0:
        await asyncio.sleep(1)
        timers[timer_id] -= 1

    del timers[timer_id]
    channel = bot.get_channel(channel_id)
    await channel.send(f"{random.choice(islands)}")

@bot.command()
@commands.has_permissions(administrator=True)
async def кв(ctx):
    result = random.randrange(1, 26)
    if result == 25:
        await ctx.reply(embed=disnake.Embed(
            description="Вам крупно повезло! \nВы стали обладателем королевской воли с рождения.",
            color=0x00ff2f
            ))
    else:
        await ctx.reply(embed=disnake.Embed(
            description="Вам не повезло :(\nВы обычный человек",
            color=0xff0000
            ))
        
@bot.command()
@commands.has_permissions(administrator=True)
async def мантра(ctx):
    result = random.randrange(1, 6)
    if result == 5:
        await ctx.reply(embed=disnake.Embed(
            description="Вам крупно повезло! \nВам крупно повезло вы стали обладателем мантры с рождения.",
            color=0x00ff2f
            ))
    else:
        await ctx.reply(embed=disnake.Embed(
            description="Вам не повезло :(\nВы не обладаете мантрой.",
            color=0xff0000
            ))
        
@bot.command()
async def ранг(ctx, member: disnake.Member=None):
    if member is None:
        cursor.execute(f"SELECT lvl FROM lvl WHERE id = {ctx.author.id}")
        lvl = cursor.fetchone()[0]
        if lvl < 200:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 1"))
        elif 300 > lvl >= 100:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 2"))
        elif 400 > lvl >= 200:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 3"))
        elif 500 > lvl >= 300:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 4"))
        elif 600 > lvl >= 400:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 5"))
        elif 700 > lvl >= 500:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 6"))
        elif 800 > lvl >= 600:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 7"))
        elif 900 > lvl >= 700:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 8"))
        elif 1000 > lvl >= 900:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 9"))
        elif lvl >= 900:
            await ctx.reply(embed=disnake.Embed(description="Вашь уровень - 10"))
    else:
        cursor.execute(f"SELECT lvl FROM lvl WHERE id = {member.id}")
        lvl = cursor.fetchone()[0]
        if lvl < 200:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 1"))
        elif 300 > lvl >= 100:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 2"))
        elif 400 > lvl >= 200:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 3"))
        elif 500 > lvl >= 300:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 4"))
        elif 600 > lvl >= 400:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 5"))
        elif 700 > lvl >= 500:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 6"))
        elif 800 > lvl >= 600:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 7"))
        elif 900 > lvl >= 700:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 8"))
        elif 1000 > lvl >= 900:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}> - 9"))
        elif lvl >= 900:
            await ctx.reply(embed=disnake.Embed(description=f"Уровень участника <@{member.id}>- 10"))

@bot.command()
@commands.cooldown(1, 300, BucketType.user)  # rate of 1 per 300 seconds (5 minutes) per user
async def рыбачить(ctx):
    cursor.execute("SELECT lvl FROM lvl WHERE id = ?", (ctx.author.id,))
    lvl = cursor.fetchone()[0]
    if lvl < 300:
        result = random.randrange(1, 4)
        if result == 1:
            embed2=disnake.Embed(
            description=f"Вы словили ботинок",
            color=0x69e6ff
            )
            embed2.set_image("https://cdn-icons-png.flaticon.com/512/7157/7157460.png")
            await ctx.reply(embed=embed2)
        elif result == 2:
            embed1=disnake.Embed(
                description=f"Вы словили консервную банку",
                color=0x69e6ff)
            embed1.set_image("https://media.discordapp.net/attachments/1126574949532962867/1128986126837891155/1674356441_papik-pro-p-konservnaya-banka-risunok-6.png?width=640&height=640")
            await ctx.reply(embed=embed1)
        elif result == 3:
            res = random.randrange(1, 5)
            if res == 1:
                embed=disnake.Embed(
                    description=f"Вы словили сельдя",
                    color=0x002fff
                )
                embed.set_image("https://images-ext-1.discordapp.net/external/in5SPbiXVtiCKMnI4Ts5PIvfKnkCk9loGM0rWl4dHJE/https/maxblogs.ru/images/157.jpg?width=800&height=600")
                await ctx.reply(embed=embed)
                cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
                connection.commit()
            elif res == 2:
                embed=disnake.Embed(
                    description=f"Вы словили амура",
                    color=0x002fff
                )
                embed.set_image("https://images-ext-2.discordapp.net/external/s3KXazv2JdxNS2WqELgxGQMc5v-iDZBTqMjcvK0RoeQ/https/image.jimcdn.com/app/cms/image/transf/none/path/s3974dcc17bc4f3da/image/i7e8ad75a6ea7190b/version/1569256427/image.jpg?width=750&height=468")
                await ctx.reply(embed=embed)
                cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
                connection.commit()
            elif res == 3:
                embed=disnake.Embed(
                    description=f"Вы словили амура",
                    color=0x002fff
                )
                embed.set_image("https://images-ext-1.discordapp.net/external/2W-7jZja_eO0U_LCGys3i1-Tb9_yGbG-SxkBjrvLypE/https/fishingday.org/wp-content/uploads/2019/02/1-1.jpg?width=1401&height=670")
                await ctx.reply(embed=embed)
                cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
                connection.commit()
            elif res == 4:
                embed=disnake.Embed(
                    description=f"Вы словили судака",
                    color=0x002fff
                )
                embed.set_image("https://images-ext-1.discordapp.net/external/VKuQGbnKbUsESIrlHl2QMRsa9XHXco3m6NQSbyVL2qE/https/spinningpro.ru/wp-content/uploads/2019/12/sudak1.jpg?width=1352&height=670")
                await ctx.reply(embed=embed)
                cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
                connection.commit()
    elif lvl >= 300 and lvl < 600:
        res1 = random.randrange(1, 4)
        if res1 == 1:
            embed5 = disnake.Embed(
                description="Вы словили небесную рыбу",
                color=0x07ebf7
            )
            embed5.set_image("https://images-ext-2.discordapp.net/external/Mpnw6cGYS7e0aRr0H-igzwoiyXfz4t57Wm6kAqDHvJU/%3Fcb%3D20100905194734%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/7/7f/Sky_Fish.jpg/revision/latest?width=800&height=600")
            await ctx.reply(embed=embed5)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif res1 == 2:
            embed6 = disnake.Embed(
                description="Вы словили бойцовскую рыбу",
                color=0xc9127a
            )
            embed6.set_image("https://images-ext-1.discordapp.net/external/VvFfqjxC3wmaE5jjY_-kuntAvEWLjhEADfKbq9V0QnI/%3Fcb%3D20150828141548%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/a/a0/Boss_Class_Fighting_Fish.png/revision/latest?width=898&height=670")
            await ctx.reply(embed=embed6)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif res1 == 3:            
            embed7 = disnake.Embed(
                description="Вы словили розарио",
                color=0x8c004f
            )
            embed7.set_image("https://images-ext-2.discordapp.net/external/4koYFcj3bfGbSCCv1GSUBDKrfX3YZnsPyH7d7m9R5zM/%3Fcb%3D20150731165544%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/8/8e/Rosario_Anime_Infobox.png/revision/latest/thumbnail/width/360/height/360?width=450&height=397")
            await ctx.reply(embed=embed7)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
    elif lvl >= 600 and lvl < 900:
        res2 = random.randrange(1, 4)
        if res2 == 1:
            embed8 = disnake.Embed(
                description="Вы словили морскую рыбу",
                color=0x427047
            )
            embed8.set_image("https://images-ext-2.discordapp.net/external/rxb0cjgjxZJB7ysP0Jzzd_DT1muH_hGJmBo6kN4UPrI/%3Fcb%3D20140711174605%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/1/16/Mohmoo_Anime_Infobox.png/revision/latest?width=737&height=598")
            await ctx.reply(embed=embed8)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif res2 == 2:
            embed9 = disnake.Embed(
                description="Вы словили пожирателя островов",
                color=0xed024d
            )
            embed9.set_image("https://images-ext-1.discordapp.net/external/gNiUDKOfZnKL9SNAGh43o476dJ12AnNR7gPvy4HHOQ0/%3Fcb%3D20171021084359%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/7/74/Island_Eater_Anime_Infobox.png/revision/latest?width=800&height=505")
            await ctx.reply(embed=embed9)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif res2 == 3:
            embed10 = disnake.Embed(
                description="Вы словили кита\nшанс `15%`",
                color=0x434c8c
            )
            embed10.set_image("https://images-ext-1.discordapp.net/external/TGztoacewbobnxwBl84XLLFMb_ZxHLd7FtXkDNQxkqM/%3Fq%3Dtbn%3AANd9GcTO8mVT6VeqN3CqAJJqlCojCddPFa-n8gd6CA%26usqp%3DCAU/https/encrypted-tbn0.gstatic.com/images?width=323&height=242")
            await ctx.reply(embed=embed10)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
    elif lvl >= 1000:
        res3 = random.randrange(1, 10002)
        if 1000 <= res3 < 1500:
            embed11 = disnake.Embed(
                description="Вы словили бонбори",
                color=0x403045
            )
            embed11.set_image("https://images-ext-2.discordapp.net/external/3o9xIcLKqFIBn4OGjmZimXh_qvGKa1hHCFejb9bYwCk/%3Fcb%3D20161021032546%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/e/e3/Bonbori_Infobox.png/revision/latest?width=670&height=670")
            await ctx.reply(embed=embed11)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif res3 == 10001:
            embed12 = disnake.Embed(
                description="Вы словили фрукт\nшанс `0.1%`",
                color=0xff6200
            )
            embed12.set_image("https://i.etsystatic.com/25590692/r/il/969b08/3903240515/il_570xN.3903240515_a50q.jpg")
            await ctx.reply(embed=embed12)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif 1500 <= res3 < 2500:
            embed13 = disnake.Embed(
                description="Вы словили короля морей\nшанс `10%`",
                color=0x023d00
            )
            embed13.set_image("https://images-ext-2.discordapp.net/external/RH_4snK4GOl_X6I8UWLLW6UgazzqkIlt_WrLF3gWSoQ/%3Fcb%3D20111219013625%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/f/f1/Lordofthecoast.jpg/revision/latest?width=640&height=480")
            await ctx.reply(embed=embed13)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif 2500 <= res3 < 6250:
            embed14 = disnake.Embed(
                description="Вы словили синего слонового тунца\nшанс `37.5%`",
                color=0x273d5c
            )
            embed14.set_image("https://images-ext-2.discordapp.net/external/m7Mg0ykLMCORrfmKdgNq99Tk3ciHnTxsZYTqkvQ6QMg/%3Fcb%3D20100905193213%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/7/78/Bluetuna.png/revision/latest?width=1440&height=308")
            await ctx.reply(embed=embed14)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()
        elif 6250 <= res3 < 10001:
            embed15 = disnake.Embed(
                description="Вы словили каменную рыбу\nшанс `37.5%`",
                color=0x273d5c
            )
            embed15.set_image("https://images-ext-2.discordapp.net/external/PvPpL7tyfFKr3MZiATR2mJmvWyKSRwAuFmavTfHEKkA/%3Fcb%3D20171105135532%26path-prefix%3Dru/https/static.wikia.nocookie.net/onepiece/images/e/eb/Armored_Stonefish.png/revision/latest/scale-to-width-down/1000?width=961&height=670")
            await ctx.reply(embed=embed15)
            cursor.execute(f"UPDATE lvl SET lvl = lvl + {1} WHERE id = {ctx.author.id}")
            connection.commit()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Команда на кулдауне, попробуйте через {:.2f}с'.format(error.retry_after))
        



            








        
            
        






bot.run(os.getenv('TOKEN'))
