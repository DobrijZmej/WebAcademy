import random
import threading
import traceback
from math import sqrt

import discord
import asyncio
import json

from pathlib import Path
import urllib.request
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import uuid

import os
os.environ["NLS_LANG"] = "UKRAINIAN_UKRAINE.CL8MSWIN1251"
import cx_Oracle

import ora_data
import sys_img

def read_config(in_server_id):
    config = {}
    if (os.path.isfile(in_server_id+'.json')):
        with open(in_server_id+'.json') as config_file:
            config = json.load(config_file)
    return config



def save_config(in_server_id, in_config):
    with open(in_server_id+'.json', 'w') as outfile:
        json.dump(in_config, outfile)

client = discord.Client()

def get_value(dict, key):
    if(key in dict):
        return dict[key]
    return ''

def get_channel_object(name):
    #print("=================")
    for server in client.servers:
        for channel in server.channels:
            #print(channel.name+" "+channel.id)
            if(channel.name == name):
                return channel

""" ================== Получение данных из Оракла ============================="""
def get_child_bodies_by_id(in_conn, in_system_id, in_parent_body, in_level, in_draw, in_img, in_y):
    tmp_str = ""
    #tmp_str = tmp_str + " " + str(in_system_id) + " " + str(in_parent_body) + "\r\n"
    sql = """/*step 2*/
    select s.id                  /*f000*/,
           b.name                /*f001*/,
           b.distance_to_arrival /*f002*/,
           g.name_ua             /*f003*/,
           b.id body_id          /*f004*/,
           st.name               /*f005*/,
           st.controlling_minor_faction_id /*f006*/,
           b.type_id             /*f007*/
    from   eddb_systems s,
           eddb_bodies b,
           eddb_groups g,
           eddb_stations st
    where  s.id=:system_id
           and b.parent_id = :parent_id
           and b.system_id(+)=s.id
           and g.id(+)=b.group_id
           and st.body_id(+)=b.id
    order by nvl(b.distance_to_arrival, 0), b.name
           """
    cur = in_conn.cursor()
    cur.execute(sql, (in_system_id, in_parent_body))
    # rows = cur.fetchall()
    font = ImageFont.truetype("imgs\\GOTHIC.TTF", 25)
    for row in cur.fetchall():
        #print(row[1])
        tmp_str = tmp_str + "   "*in_level + str(row[3]) + ' ' + str(row[1]) + ', відстань ' + "{:,}".format((row[2] or 0))
        if(row[5] is not None):
            tmp_str = tmp_str + ", є станція " + str(row[5]) + ", що належить фракції " + str(row[6])
        tmp_str = tmp_str + '\r\n'

        #print("imgs\\planets\\" + str(row[7]) + ".png")
        if (os.path.isfile("imgs\\planets\\" + str(row[7]) + ".png")):
            img_star = Image.open("imgs\\planets\\" + str(row[7]) + ".png")
            img_star = img_star.resize((22, 22))
            in_img.paste(img_star, (10*in_level, in_y[0] + 3))
        str_image = "   "*in_level + str(row[3]) + ' ' + str(row[1]) + ', відстань ' + "{:,}".format((row[2] or 0))
        in_draw.text((30, in_y[0]), str_image, (255, 255, 0), font=font)
        in_y[0] = in_y[0]+25

        tmp_str = tmp_str + get_child_bodies_by_id(in_conn, row[0], row[4], in_level+1, in_draw, in_img, in_y)

    return tmp_str

""" ================== Базовые сведения по системе ============================="""
async def get_system_from_oracle(message, in_system_name):
    new_ora = ora_data.ora_data()
    print(new_ora.find_system_by_name(in_system_name))
    print(new_ora.get_system_base_info(in_system_name))
    try:
        connection = cx_Oracle.connect('c##dobrijzmej', '7014258', 'ZMEJ')
    except cx_Oracle.DatabaseError as exception:
        await client.send_message(message.channel, message.author.mention + 'Failed to connect to ZMEJ')
        print('Failed to connect to %s\n', 'ZMEJ')
        traceback.print_exc()
        #printException(exception)
        return
    sql = """/*step 1*/
select s.id                  /*f000*/,
       b.name                /*f001*/,
       b.distance_to_arrival /*f002*/,
       g.name_ua             /*f003*/,
       b.id body_id          /*f004*/,
       g.name                /*f005*/,
       b.spectral_class      /*f006*/
from   eddb_systems s,
       eddb_bodies b,
       eddb_groups g
where  s.name=:name
       and b.system_id(+)=s.id
       and b.parent_id is null
       and g.id(+)=b.group_id
order by b.name
       """

    level = 0
    str_bodies = ""
    str_image = ""
    font = ImageFont.truetype("imgs\\GOTHIC.TTF", 25)
    img = Image.open("imgs\\system_background_001.png")
    draw = ImageDraw.Draw(img)
    y = [0];

    cur = connection.cursor()
    cur.execute(sql, name=in_system_name)
    #rows = cur.fetchall()
    for row in cur.fetchall():
        print(row[1])
        str_image = str(row[3])+' '+str(row[1])
        if(str(row[5]) == 'Star'):
            str_image = str_image+' клас '+str(row[6])
            if(os.path.isfile("imgs\\stars\\"+str(row[6])+".png")):
                img_star = Image.open("imgs\\stars\\"+str(row[6])+".png")
                img_star = img_star.resize((22, 22))
                img.paste(img_star, (2, y[0]+3))
        str_image = str_image+', відстань '+"{:,}".format((row[2] or 0))

        #str_bodies = str_bodies+str(row[3])+' '+str(row[1])
        #if(str(row[5]) == 'Star'):
        #    str_bodies = str_bodies+' клас '+str(row[6])
        #str_bodies = str_bodies+', відстань '+str(row[2])#+'\n'
        str_bodies = str_bodies + str_image + '\r\n'
        print(str_image)

        draw.text((30, y[0]), str_image, (255, 255, 0), font=font)
        y[0] = y[0] + 25
        str_bodies = str_bodies +get_child_bodies_by_id(connection, row[0], row[4], level+1, draw, img, y)
    #str_bodies = str(cur.fetchone())
    #await client.send_message(message.channel, str(message.author.mention + " об'єкти в системі:\r\n"+str_bodies)[:2000])
    #await client.send_file(message.channel, 'imgs\\system_background_001.png')

    #draw.multiline_text((0, 0), str_bodies, (255, 255, 0), font=font)
    #draw.text((0, 0), str_bodies, (255, 255, 0), font=font)
    #draw = ImageDraw.Draw(img)
    #draw = ImageDraw.Draw(img)

    #img_star = Image.open("imgs\\start\\A.png")
    #img_star = img_star.resize((25, 25))
    #img.paste(img_star, (300, 300))
    #img = img.alpha_composite(img, img_star)

    image_file = "tmp\\"+uuid.uuid4().hex+".png"
    img.save(image_file)

    await client.send_file(message.channel, image_file)


@client.event
async def on_ready():
    print('Loggid in as')
    print(client.user.name)
    print(client.user.id)
    print('----------')
    discord.Status
    #bot_game = discord.Game(name="Єдина Україна", url="http://ed.dobrijzmej.org", type=0)
    #await client.change_presence(game=bot_game)

@client.event
async def on_message(message):

    config = read_config(message.server.id)
    prefix = get_value(config, 'prefix')
    if(prefix == ''):
        prefix = '!'

    if client.user.mentioned_in(message):
        await on_mention_me(message)

    if message.content.startswith(prefix+"допомога"):
        await on_help(message)
    if message.content.startswith(prefix+"допоможи"):
        await on_help(message)
    if message.content.startswith(prefix+"help"):
        await on_help_en(message)
    if message.content.startswith(prefix+"статистика"):
        await on_statistic(message)
    if message.content.startswith(prefix+"стат"):
        await on_statistic(message)
    if message.content.startswith(prefix+"знайти"):
        await on_find(message)
    if message.content.startswith(prefix+"знайди"):
        await on_find(message)
    if message.content.startswith(prefix+"де"):
        await on_find(message)
    if message.content.startswith(prefix+"система"):
        await on_find_system(message, 'ua')
    if message.content.startswith(prefix+"system"):
        await on_find_system(message, 'en')
    if message.content.startswith(prefix+"відстань"):
        await on_distance_systems(message, 'ua')
    if message.content.startswith(prefix+"вiдстань"):
        await on_distance_systems(message, 'ua')
    if message.content.startswith(prefix+"distance"):
        await on_distance_systems(message, 'en')
    if message.content.startswith(prefix+"я "):
        await on_safe_cmdr_name(message)
    if message.content.startswith(prefix+"переклади "):
        await on_translate(message)
    if message.content.startswith(prefix+"setprefix "):
        await on_setprefix(message)
    if message.content.startswith(prefix + "місії за сьогодні"):
        await on_get_missions_on_day(message)
    if message.content.startswith(prefix + "миссии за сегодня"):
        await on_get_missions_on_day(message)
    if message.content.startswith(prefix + "нагороди за сьогодні"):
        await on_get_bountys_on_day(message)
    if message.content.startswith(prefix + "награды за сегодня"):
        await on_get_bountys_on_day(message)
    if message.content.startswith(prefix + "мої місії"):
        await on_get_my_missions(message)
    if message.content.startswith(prefix + "мої нагороди"):
        await on_get_my_bountys(message)
    if message.content.startswith(prefix + "мої вбивства"):
        await on_get_ship_kills_on_day(message)
    if message.content.startswith(prefix + "мої стрибки"):
        await on_get_distance_on_day(message)



    if(message.content.lower().find('слава україні')>=0):
        await client.send_message(message.channel,message.author.mention + ", Героям Слава!")
    if(message.content.lower().find('слава украине')>=0):
        await client.send_message(message.channel,message.author.mention + ", Героям Слава!")
    """g_channel = client.get_all_channels()"""
    """print(str(g_channel[0]))"""
    #print(get_channel_id('general'))


@client.event
async def on_member_join(member):
    #print(get_channel_id('general'))
    await client.send_message(get_channel_object('bots'), member.mention + ", ласкаво просимо до серверу української спільноти гри Elite Dangerous!\r\nЯ можу тобі дещо підказати, якщо ти напишеш `!допомога`")

@client.event
async def on_member_remove(member):
    await client.send_message(get_channel_object('bots'), member.mention + " покинув наш сервер.")

@client.event
async def on_member_update(before, after):
    #print(after.game)
    if(after.game != before.game):
        #print(str(after.display_name))
        #print(str(before.display_name))
        #print(str(after.server.id))
        if(str(after.server.id)!='276054497716076546'):
            return
        print(str(after.display_name) + " open "+str(after.game))
        if(str(after.game).lower() == "elite: dangerous" or str(after.game).lower() == "elite dangerous"):
            prefix = ["зійшов на місток", "увійшов до", "піднявся на борт свого корабля у", "щойно запустив", "вже у"]
            prefix_index = random.randint(0, len(prefix)-1)
            #await client.send_message(message.channel, message.author.mention+", "+prefix[prefix_index]+' "'+j_adages['adages'][adage_index]+'"')
            await client.send_message(get_channel_object('bots'), str(after.display_name) + " "+prefix[prefix_index]+" "+str(after.game))

"""if(message.author.id != client.user.id):
       print(message.content)
       print(message.author.id)
       print(*message.mentions, sep='\n')
       if client.user.mentioned_in(message):
           await on_mention_me(message)
           print('mention me')
       #await client.send_message(message.channel, message.author.mention+", "+message.content)
       em = discord.Embed(title='Довідкова інформація', description=message.content+", повідомив "+message.author.mention, colour=0xDEADBF)
       em.set_author(name='Космічний козак', icon_url=client.user.default_avatar_url)
       await client.send_message(message.channel, embed=em)"""

""" ================== помощь ============================="""
async def on_help(message):
    em = discord.Embed(title='Перелік відомих мені команд:', colour=0xDEADBF)
    #em.set_author(name='Космічний козак', icon_url=client.user.avatar_url)
    em.add_field(name="!допомога, !допоможи", value="```Показує це повідомлення```", inline=True)
    em.add_field(name="!де, !знайди, !знайти", value="```Шукає пілота на сайті edsm.net, та відображає, де його бачили востаннє```", inline=True)
    em.add_field(name="!система", value="```Шукає систему на сайті eddb.io, та відображає перелік назв, які підходять под пошук. Якщо якась система має таку повну назву, то відображає посилання на її опис, та кратку інформацію про неї```", inline=True)
    em.add_field(name="!відстань", value="```Використання: !відстань система1 до система2\r\nШукає координати систем у базі, та якщо системи знайдені, вираховує відстань між ними.```", inline=True)
    em.add_field(name="!переклади", value="```Використання: !переклади чай, !переклади data\r\nШукаю вказану назву в торгівельних товарах та в матеріалах, і виводжу переклад на іншу мову.```", inline=True)
    await client.send_message(message.channel, embed=em)
    if(message.channel.name.lower() == 'tactic_strategic'):
        em = discord.Embed(title='Таємні команди:', colour=0xDEADBF)
        em.add_field(name="!місії за сьогодні, !миссии за сегодня", value="```Показую статистику за сьогодні по спільноті.```", inline=True)
        em.add_field(name="!нагороди за сьогодні, !награды за сегодня", value="```Показую статистику за сьогодні по спільноті.```", inline=True)
        await client.send_message(message.channel, 'Таємні команди:\r\n```' + \
        					   '!місії за сьогодні, !миссии за сегодня: Показую статистику за сьогодні по спільноті.\r\n' + \
        				           "!нагороди за сьогодні, !награды за сегодня: Показую статистику за сьогодні по спільноті.```")
    if(message.channel.name.lower() == 'uca_ukrainian_colonist'):
        await client.send_message(message.channel, "Таємні команди:\r\n```" + \
                                               "!мої місії    Показую статистику за сьогодні по пілоту.\r\n"+ \
                                               "!мої нагороди Показую статистику за сьогодні по пілоту.\r\n"+ \
                                               "!мої вбивства Показую, які кораблі ти сьогодні знищив, яку кількість, та скількі грошей отримав.\r\n"+ \
                                               "!мої стрибки  Показую, скільки гіперстрибків ти зробив, яка загальна відстань, та скільки палива витратив.\r\n"+ \
                                               "```")
""" ================== help ============================="""
async def on_help_en(message):
    config = read_config(message.server.id)
    prefix = get_value(config, 'prefix')
    if(prefix == ''):
        prefix = '!'
    em = discord.Embed(title='List of commands that I know:', colour=0xDEADBF)
    #em.set_author(name='Космічний козак', icon_url=client.user.avatar_url)
    em.add_field(name=prefix+"setprefix", value="```Change the first symbol of my command```", inline=False)
    em.add_field(name=prefix+"help", value="```Shows this message```", inline=False)
    em.add_field(name=prefix+"distance", value="```using: "+prefix+"distance system1 : system2\r\nSearches the coordinates of the system in the database, and if the systems are found, it calculates the distance between them in a straight line, and gives a link to the map showing the indicated systems.```", inline=True)
    em.add_field(name=prefix+"system", value="```using: "+prefix+"system Colonia\r\nShow system map (command in develop).```", inline=True)
    await client.send_message(message.channel, embed=em)

""" ================== статистика ============================="""
async def on_statistic(message):
    f_server_config = Path(message.server.id+".json")
    if(not f_server_config.is_file()):
        j_server_config = {}
        j_server_config["server name"] = message.server.name
        j_server_config["statistic"] = {}
        j_server_config["statistic"]["all"] = 0
        j_server_config["statistic"]["own"] = 0
        j_server_config["statistic"]["ships"] = 0
        with open(message.server.id+".json", 'w') as outfile:
           json.dump(j_server_config, outfile)
    with open(message.server.id + ".json", 'r') as outfile:
        j_server_config = json.loads(outfile.read())

    em = discord.Embed(title='Статистика', description=message.author.mention+", взагалі "+j_server_config["statistic"]["all"]+', наших '+j_server_config["statistic"]["own"]+', кораблів '+j_server_config["statistic"]["ships"], colour=0xDEADBF)
    em.set_author(name='Космічний козак', icon_url=client.user.avatar_url)
    #em.set_author(name='Космічний козак', icon_url=discord.Server.icon)
    await client.send_message(message.channel, embed=em)
    #await client.send_message(message.channel, message.author.mention+", взагалі "+j_server_config["statistic"]["all"]+', наших '+j_server_config["statistic"]["own"]+', кораблів '+j_server_config["statistic"]["ships"])

    #print("0", j_server_config)
    #if(exists)
    #with open('adages1.json', 'r') as f_adages:
    args = message.content.split()
    if(len(args) == 4):
        j_server_config["statistic"]["all"] = args[1]
        j_server_config["statistic"]["own"] = args[2]
        j_server_config["statistic"]["ships"] = args[3]
        #print("0", j_server_config)
        with open(message.server.id+".json", 'w') as outfile:
            json.dump(j_server_config, outfile)
        await client.send_message(message.channel,
                                  message.author.mention + ", записав: "+
                                  "взагалі " + j_server_config["statistic"]["all"] +
                                  ', наших ' + j_server_config["statistic"]["own"] +
                                  ', кораблів ' + j_server_config["statistic"]["ships"]+". Дякую!")
            #print("1", args)
            #print("2", message.server)

""" ================== обращение к роботу ============================="""
async def on_mention_me(message):
    print(message.server.name)
    print(message.content)
    if(str(message.server.id) != '276054497716076546'):
        return 0
    args = message.content.split()
    if(args[1] == 'help'):
        await on_help_en(message)
        return

    with open('adages.json', 'r') as f_adages:
        j_adages = json.loads(f_adages.read())
    #print(len(j_adages['adages']))
    adage_index = random.randint(0, len(j_adages['adages'])-1)
    prefix = ["як казав мій батько,", "древні казали:", "колись в космічному просторі почув, що", "у Києві кажуть, що", "чи знаєте ви, що"]
    prefix_index = random.randint(0, len(prefix)-1)
    #print(prefix_index)
    await client.send_message(message.channel, message.author.mention+", "+prefix[prefix_index]+' "'+j_adages['adages'][adage_index]+'"')

""" ================== поиск командира ============================="""
async def on_find(message):
    print(message.content)
    args = message.content.split()
    print(len(args))
    commander_name = ""
    for n in args[1:]:
        if(commander_name!=''):
            commander_name += "+"
        commander_name += n
    if(commander_name == "я"):
        commander_name = read_param(message.server.id, "CMDR_"+message.author.id).replace(" ", "+")
        if(commander_name==""):
            await client.send_message(message.channel, message.author.mention + ", нажаль, я поки що так близько з тобою не знайомий. Але можемо познайомитися, якщо ти напишешь ""**!я твій нік**""")
            return
    print(commander_name)
    if(commander_name[0:2] == "<@"):
        commander_name = commander_name.replace("<@!", "").replace("<@", "")
        print('finding commander '+"CMDR_"+commander_name[:-1])
        commander_name = read_param(message.server.id, "CMDR_"+commander_name[:-1]).replace(" ", "+")
        if(commander_name==""):
            await client.send_message(message.channel, message.author.mention + ", нажаль, я щє не знайомий ц зим командиром. Але ми можемо познайомитися, якщо він напише ""!я його нік""")
            return

    em = discord.Embed(title='Інформація про пілота '+commander_name.replace("+", " ")+' за даними сайту edsm.net:', colour=0xDEADBF)

    print("https://www.edsm.net/api-commander-v1/get-ranks?commanderName="+commander_name)
    result = urllib.request.urlopen("https://www.edsm.net/api-commander-v1/get-ranks?commanderName="+commander_name).read()
    print(result.decode('ascii'))
    result = json.loads(result.decode('ascii'))
    s_rangs = ""
    if(result['msgnum'] == 100):
        s_system = '[інформація закрита пілотом]'
        if('ranksVerbose' in result):
        #if (not result['ranksVerbose'] is None):
            s_system = result['ranksVerbose']
            s_rangs = "```Бойовий       : "+str(get_value(result['ranks'], 'Combat'    )) +" "+s_system['Combat']    +", "+str(get_value(result['progress'], 'Combat'))+"%"+"\r\n"+\
                         "Торговий      : "+str(get_value(result['ranks'], 'Trade'     )) +" "+s_system['Trade']     +", "+str(get_value(result['progress'], 'Trade'))+"%"+"\r\n"+\
                         "Дослідницький : "+str(get_value(result['ranks'], 'Explore'   )) +" "+s_system['Explore']   +", "+str(get_value(result['progress'], 'Explore'))+"%"+"\r\n"+\
                         "CQC           : "+str(get_value(result['ranks'], 'CQC'       )) +" "+s_system['CQC']       +", "+str(get_value(result['progress'], 'CQC'))+"%"+"\r\n"+\
                         "У федерації   : "+str(get_value(result['ranks'], 'Federation')) +" "+s_system['Federation']+", "+str(get_value(result['progress'], 'Federation'))+"%"+"\r\n"+\
                         "У імперії     : "+str(get_value(result['ranks'], 'Empire'    )) +" "+s_system['Empire']    +", "+str(get_value(result['progress'], 'Empire'))+"%"+"```"
    else:
        s_rangs = ""

    if(s_rangs != ''):
       em.add_field(name="Ранги пілота:", value=s_rangs, inline=False)

    print("send query https://www.edsm.net/api-logs-v1/get-position?commanderName="+commander_name)
    result = urllib.request.urlopen("https://www.edsm.net/api-logs-v1/get-position?commanderName="+commander_name).read()
    print(result.decode('ascii'))
    result = json.loads(result.decode('ascii'))
    s_pilot_coords = ""
    if(result['msgnum'] == 100):
        s_system = '[інформація закрита пілотом]'
        if(not result['system'] is None):
            s_system = result['system']
        s_date = '[інформація закрита пілотом]'
        if (not result['date'] is None):
            s_date = result['date']

        s_pilot_coords = "Система **"+s_system+"**, і це було **"+s_date+"**."
        #print(s_pilot_coords)
        em.add_field(name="Останні відомі координати пілота:", value=s_pilot_coords, inline=False)
        if(get_value(result, 'url')!=''):
           em.add_field(name="Профіль пілота:", value=get_value(result, 'url').replace("/en/", "/uk/"), inline=False)
        s_image = get_value(result, 'url')[40:]
        s_image = s_image[:s_image.find("/")]
        if(s_image != ''):
            print(s_image)
            s_image2 = ""
            for r in s_image[0:]:
                s_image2 = s_image2 + r + "/"
                print(r)
            print("https://www.edsm.net/img/users/" + s_image2 + s_image + ".jpg")
            em.set_thumbnail(url="https://www.edsm.net/img/users/" + s_image2 + s_image + ".jpg?v="+str(random.randint(0, 9999999)))

            print("send query https://www.edsm.net/uk/statistics/user/credits/id/"+s_image)
            result = urllib.request.urlopen("https://www.edsm.net/uk/statistics/user/credits/id/"+s_image).read()
            if(result.decode('ascii')):
                result = json.loads(result.decode('ascii'))
                if(result['balance']):
                    if(result['balance'][-1]):
                        if(result['balance'][-1]['y']):
                            print(str(result['balance'][-1]['y']))
                            em.add_field(name="Поточний баланс грошей:", value="{:,}".format(result['balance'][-1]['y']), inline=False)

    else:
        #s_pilot_coords = "Нажаль, при пошуку пілота сталася помилка: "+result['msg'];
        em.add_field(name="Сталася помилка:", value=result['msg'], inline=False)
        #await client.send_message(message.channel, message.author.mention+", нажаль, при пошуку пілота сталася помилка: "+result['msg'])


    await client.send_message(message.channel, embed=em)

""" ================== поиск системы ============================="""
async def on_find_system_edsm(message, systemName):


    url = "https://www.edsm.net/api-v1/system?systemName=" + systemName.replace(" ", "+") + "&showId=1&showCoordinates=1&showInformation=1"
    print("send query " + url)
    resultEdsm = urllib.request.urlopen(url).read()
    print(resultEdsm.decode('ascii'))
    resultJson = json.loads(resultEdsm)
    print(len(resultJson))
    #print(str(resultJson['id']))
    em = discord.Embed(title='За даними сайту edsm.net https://www.edsm.net/uk/system/id/'+str(resultJson['id'])+'/name/'+systemName.replace(" ", "+")+':', colour=0xDEADBF)
    em.set_author(name='Космічний козак', icon_url=client.user.avatar_url)
    galaxy_map = ""
    if(len(resultJson['coords']) > 0):
       em.add_field(name="Координати системи:",
                    value="x: "+str(resultJson['coords']['x'])+"\r\ny: "+str(resultJson['coords']['y'])+"\r\nz: "+str(resultJson['coords']['z']),
                    inline=True)
       galaxy_map ="https://ed.dobrijzmej.org/map/?system="+systemName.replace(" ", "%20")+";"+str(resultJson['coords']['x'])+";"+str(resultJson['coords']['y'])+";"+str(resultJson['coords']['z'])
    else:
        em.add_field(name="Координати системи:", value="невідомі", inline=True)
    if(len(resultJson['information']) > 0):
        em.add_field(name="Інформація:", value="Сила: "+     str(get_value(   resultJson['information'], 'allegiance'))+"\r\n"+
                                               "Уряд: "+     str(get_value(   resultJson['information'], 'government'))+"\r\n"+
                                               "Фракція: "+  str(get_value(   resultJson['information'], 'faction'))+"\r\n"+
                                               "Стан: "+     str(get_value(   resultJson['information'], 'state'))+"\r\n"+
                                               "Населення: "+format(get_value(resultJson['information'], 'population'), ',d')+"\r\n"+
                                               "Безпека: "+  str(get_value(   resultJson['information'], 'security'))+"\r\n"+
                                               "Економіка: "+str(get_value(   resultJson['information'], 'economy')), inline=True)
    else:
        em.add_field(name="Інформація:", value="відсутня", inline=True)
    if(galaxy_map!=""):
        em.add_field(name="Посилання на галактичній мапі:", value=galaxy_map, inline=True)
    await client.send_message(message.channel, embed=em)

    await get_system_from_oracle(message, systemName)

""" ================== Построение изображения системы ============================="""
def system_build_image(in_system_info, in_ora_connect):
    """ ================== Построение изображения системы ============================="""
    system_img = sys_img.sys_img()

        # нарисовали заголовок
    system_img.create_title(in_system_info)
        # нарисовали карту системы
    system_img.create_galaxy_map(in_system_info["X"], in_system_info['Z'], in_system_info['SYSTEM_NAME'])
        # нарисовали звёзды
    main_bodies = in_ora_connect.get_system_main_bodies(in_system_info['ID'])
    system_img.fill_main_bodys(main_bodies)
        # для каждой звезды рисуем перечень планет
    for i, body in main_bodies.items():
        print(body)
        child_bodies = in_ora_connect.get_child_bodies(body['ID'], body['BODY_ID'])
        #print()
        system_img.fill_level_1(i, child_bodies)
        for i1, body1 in child_bodies.items():
            #print('level2: '+str(body1))
            child_bodies1 = in_ora_connect.get_child_bodies(body['ID'], body1['BODY_ID'])
            system_img.fill_level_2([i1], child_bodies1)
            print('level2: '+str(child_bodies1))

    image_file = "tmp\\"+uuid.uuid4().hex+".png"
    system_img.save(image_file)
    return image_file

""" ================== поиск системы в оракле, итоговый интерфейс ============================="""
async def on_find_system_ora(message, in_lang):
        # определим имя системы, которое ищем
    #print(message.content)
    args = message.content.split()
    #print(len(args))
    in_system_name = ""
    for n in args[1:]:
        if(in_system_name!=''):
            in_system_name += " "
        in_system_name += n

        # спросим у Оракла, знает ли он такую систему
    new_ora = ora_data.ora_data()
    m_systems_count = new_ora.find_system_by_name(in_system_name)
    print(m_systems_count)
    m_system_info = None
    if(m_systems_count['this_system'] == 1):
        await client.send_typing(message.channel)
        m_system_info = new_ora.get_system_base_info(in_system_name)
        print(m_system_info)

        m_system_bodies_stat = new_ora.get_system_groups_bodies(m_system_info[0]['ID'])
        msg_bodies_stat = ""
        for i, row in m_system_bodies_stat.items():
            if(in_lang == 'ua'):
                msg_bodies_stat = msg_bodies_stat + str(row['COUNT_BODIES']) + " " + row['NAME_UA'].lower() + ', '
            else:
                msg_bodies_stat = msg_bodies_stat + str(row['COUNT_BODIES']) + " " + row['NAME'].lower() + ', '
        msg_bodies_stat = msg_bodies_stat[:-2]
        print(msg_bodies_stat)

        m_system_bodies_stat = new_ora.get_system_stations(m_system_info[0]['ID'])
        msg_stations = ""
        for i, row in m_system_bodies_stat.items():
            msg_stations = msg_stations + str(row['NAME']) + " (" + (row['TYPE'] or "").lower() + '), '
        msg_stations = msg_stations[:-2]
        print(msg_stations)

        #print(msg[:-2])
        if(in_lang == 'ua'):
            await client.send_message(message.channel, message.author.mention + ", систему знайдено, посилання на сторонні сайти:\r\n"+
                                      "<https://eddb.io/system/" + str(m_system_info[0]['ID'])+">\r\n"+
                                      "<https://www.edsm.net/uk/system/id/" + str(m_system_info[0]['EDSM_ID']) + '/name/' + m_system_info[0]['SYSTEM_NAME'].replace(" ", "+")+'>\r\n'+
                                      "<https://ed.dobrijzmej.org/map/?system=" + m_system_info[0]['SYSTEM_NAME'].replace(" ","%20") + ";" + str(m_system_info[0]['X']) + ";" + str(m_system_info[0]['Y']) + ";" + str(m_system_info[0]['Z'])+'>\r\n'+
                                      "В системі знайдено: "+msg_bodies_stat+"\r\n"+
                                      "І станції: "+msg_stations
            )
        else:
            await client.send_message(message.channel,
                                      message.author.mention + ", system found, links to third-party sites:\r\n" +
                                      "<https://eddb.io/system/" + str(m_system_info[0]['ID']) + ">\r\n" +
                                      "<https://www.edsm.net/uk/system/id/" + str(
                                          m_system_info[0]['EDSM_ID']) + '/name/' + m_system_info[0][
                                          'SYSTEM_NAME'].replace(" ", "+") + '>\r\n' +
                                      "<https://ed.dobrijzmej.org/map/?system=" + m_system_info[0][
                                          'SYSTEM_NAME'].replace(" ", "%20") + ";" + str(
                                          m_system_info[0]['X']) + ";" + str(m_system_info[0]['Y']) + ";" + str(
                                          m_system_info[0]['Z']) + '>\r\n' +
                                      "Found in the system: " + msg_bodies_stat + "\r\n" +
                                      "and stations: " + msg_stations
                                      )
        await client.send_typing(message.channel)
        file_name = system_build_image(m_system_info[0], new_ora)
        await client.send_file(message.channel, file_name)

    elif(m_systems_count['this_system'] > 1):
        m_system_info = new_ora.get_system_base_info(in_system_name)
        #print(m_system_info)
        for i, row in m_system_info.items():
            await client.send_message(message.channel, message.author.mention + ", знайдено "+str(m_systems_count['this_system'])+" таких системи, ось посилання на сторонні сайти системи номер "+str(i+1)+":\r\n" +
                                      "<https://eddb.io/system/" + str(row['ID']) + ">\r\n" +
                                      "<https://www.edsm.net/uk/system/id/" + str(row['EDSM_ID']) + '/name/' + row['SYSTEM_NAME'].replace(" ", "+") + '>\r\n'+
                                      "https://ed.dobrijzmej.org/map/?system=" + row['SYSTEM_NAME'].replace(" ","%20") + ";" + str(row['X']) + ";" + str(row['Y']) + ";" + str(row['Z'])
                                      #"В системі знайдено: "+msg_bodies_stat+"\r\n"+
                                      #"І станції: "+msg_stations
                                      )
            #await client.send_message(message.channel, message.author.mention + ", є "+str(m_systems_count['this_system'])+" систем з таким однаковим ім'ям, але я поки що не можу надати інформацію по всім одночасно.")
            await client.send_typing(message.channel)
            file_name = system_build_image(row, new_ora)
            await client.send_file(message.channel, file_name)
    else:
        if(m_systems_count['like_systems'] == 0):
            if(in_lang == 'ua'):
                await client.send_message(message.channel, message.author.mention + ", нажаль, жодної системи з такою назвою я не знайшов...")
            else:
                await client.send_message(message.channel, message.author.mention + ", I did not find any system with such a name...")
        else:
            if(in_lang == 'ua'):
                await client.send_message(message.channel, message.author.mention + ", саме таку систему не знайдено, але є "+str(m_systems_count['like_systems'])+" зі схожою назвою: " + m_systems_count['like_systems_list'])
            else:
                await client.send_message(message.channel, message.author.mention + ", it is not such a system, but there is " + str(m_systems_count['like_systems']) + " with a similar name: " + m_systems_count['like_systems_list'])
        return


""" ================== поиск системы ============================="""
async def on_find_system(message, in_lang):
    await client.send_typing(message.channel)
    await on_find_system_ora(message, in_lang)

    return

    print(message.content)
    args = message.content.split()
    print(len(args))
    system_name = ""
    for n in args[1:]:
        if(system_name!=''):
            system_name += " "
        system_name += n


    url = "https://eddb.io/system/search?system[name]="+system_name.replace(' ', '+')+"&expand=stations&system[version]=2"
    print("send query "+url)
    result = urllib.request.urlopen(url).read()
    print(result.decode('ascii'))

    system_list = json.loads(result.decode('ascii'))

    system_fined = False
    my_system = None
    if(len(system_list) == 1):
        system_fined = True
        my_system = system_list[0]
    if(len(system_list) > 1):
        system_names = ''
        for n in system_list:
            if(system_name.lower() == n['name'].lower()):
                system_fined = True
                my_system = n
            if(system_names != ''):
                system_names += ', '
            system_names += n['name']
        await client.send_message(message.channel, message.author.mention + ", знайдено " + str(len(system_list)) + " систем: "+system_names)

    if(system_fined):
        print(str(my_system))
        stantions_list = my_system['stations']
        station_names = ''
        for n in stantions_list:
            if(station_names != ''):
                station_names += ', '
            station_names += n['name']
        station_postfix = 'станцій'
        if(len(stantions_list) == 1):
            station_postfix = 'станція'
        elif(len(stantions_list) in (2, 3, 4)):
            station_postfix = 'станції'

        if (len(system_list) > 1):
            await client.send_message(message.channel, message.author.mention + ", також знайдено систему саме з таким ім'ям: https://eddb.io/system/"+str(my_system['id'])+", у системи є "+str(len(stantions_list))+" "+station_postfix+": "+station_names)
            await on_find_system_edsm(message, my_system['name'])
        else:
            await client.send_message(message.channel, message.author.mention + ", систему знайдено: https://eddb.io/system/"+str(my_system['id'])+", у системи є "+str(len(stantions_list))+" "+station_postfix+": "+station_names)
            await on_find_system_edsm(message, my_system['name'])
    else:
        await client.send_message(message.channel, message.author.mention + ", нажаль, система з таким ім'ям не знайдена")


""" ================== расстояние между системами ============================="""
async def on_distance_systems(message, in_lang):
    print(message.content)
    systemName1 = ''
    systemName2 = ''
    systemStep = 1
    args = message.content.split()
    if(in_lang == 'ua'):
        suffix = 'до'
    else:
        suffix = ':'
    for n in args[1:]:
        if(n.lower() == suffix):
            systemStep = 2
        else:
            if(systemStep == 1):
                if(systemName1!=''):
                    systemName1 += "+"
                systemName1 += n
            else:
                if (systemName2 != ''):
                    systemName2 += "+"
                systemName2 += n
    print("systemName1="+systemName1)
    print("systemName2="+systemName2)
    if(systemName1 == ''):
        if(in_lang == 'ua'):
            await client.send_message(message.channel,message.author.mention + ", ім'я першої системи не знайдено, треба вказати ім'я систем, між якими треба розрахувати відстань, наприклад !відстань Sol до Colonia")
        else:
            await client.send_message(message.channel,message.author.mention + ", the name of the first system is not found, you must specify the name of the systems between which to calculate the distance, for example !distance Sol : Colonia")
    elif(systemName2 == ''):
        if(in_lang == 'ua'):
            await client.send_message(message.channel,message.author.mention + ", ім'я другої системи не знайдено, треба вказати ім'я систем, між якими треба розрахувати відстань, наприклад !відстань Sol до Colonia")
        else:
            await client.send_message(message.channel,message.author.mention + ", the name of the second system is not found, you must specify the name of the systems between which to calculate the distance, for example !distance Sol : Colonia")
    else:
        coord1 = {"x":0, "y": 0, "z": 0}
        coord2 = {"x":0, "y": 0, "z": 0}
        url = "https://www.edsm.net/api-v1/system?systemName=" + systemName1 + "&showCoordinates=1"
        resultEdsm = urllib.request.urlopen(url).read()
        resultJson = json.loads(resultEdsm)
        if(not resultJson):
            await client.send_message(message.channel, message.author.mention + ", система " + systemName1.replace("+", " ") + " не знайдена.")
            return
        coord1['x'] = resultJson['coords']['x']
        coord1['y'] = resultJson['coords']['y']
        coord1['z'] = resultJson['coords']['z']
        print(coord1)
        url = "https://www.edsm.net/api-v1/system?systemName=" + systemName2 + "&showCoordinates=1"
        resultEdsm = urllib.request.urlopen(url).read()
        resultJson = json.loads(resultEdsm)
        if(not resultJson):
            await client.send_message(message.channel, message.author.mention + ", система " + systemName2.replace("+", " ") + " не знайдена.")
            return
        coord2['x'] = resultJson['coords']['x']
        coord2['y'] = resultJson['coords']['y']
        coord2['z'] = resultJson['coords']['z']
        print(coord2)
        coord3 = {"x": coord1['x']-coord2['x'], "y": coord1['y']-coord2['y'], "z": coord1['z']-coord2['z']}
        coord3 = {"x": pow(coord3['x'], 2), "y": pow(coord3['y'], 2), "z": pow(coord3['z'], 2)}
        print(str(sqrt(coord3['x']+coord3['y']+coord3['z'])))

        galaxy_map = "https://ed.dobrijzmej.org/map/?system=" + systemName1.replace(" ", "%20") + ";" + str(coord1['x']) + ";" + str(coord1['y']) + ";" + str(coord1['z'])+\
                     "&system2="+systemName2.replace(" ", "%20") + ";" + str(coord2['x']) + ";" + str(coord2['y']) + ";" + str(coord2['z'])

        """await client.send_message(message.channel,message.author.mention + ", відстань від "+systemName1.replace("+", " ")+" ["+str(coord1)+"] до "+systemName2.replace("+", " ")+" ["+str(coord2)+"] дорівнює "+format(sqrt(coord3['x']+coord3['y']+coord3['z']), ',f')+" світлових років.")"""
        if(in_lang == 'ua'):
            await client.send_message(message.channel,message.author.mention + ", відстань від "+systemName1.replace("+", " ")+" до "+systemName2.replace("+", " ")+" дорівнює "+format(sqrt(coord3['x']+coord3['y']+coord3['z']), ',f')+" світлових років.\r\nПосилання на мапу: "+galaxy_map)
        else:
            await client.send_message(message.channel,message.author.mention + ", distance from "+systemName1.replace("+", " ")+" to "+systemName2.replace("+", " ")+" is "+format(sqrt(coord3['x']+coord3['y']+coord3['z']), ',f')+" ly.\r\nLink to the map: "+galaxy_map)

def read_param(in_server_id, in_param, in_value=""):
    with open(in_server_id+".json") as json_file:
        params = json.load(json_file)
    if(in_param in params):
       return params[in_param]
    else:
        return ""

def write_param(in_server_id, in_param, in_value=""):
    with open(in_server_id+".json") as json_file:
        params = json.load(json_file)
    params[in_param] = in_value
    with open(in_server_id+".json", 'w') as outfile:
        json.dump(params, outfile)

""" ================== сохранить имя командира ============================="""
async def on_safe_cmdr_name(message):
    """in_server, in_cmdr_mention, in_cmdr_name"""
    current_name = read_param(message.server.id, "CMDR_"+message.author.id)
    print("current_name="+current_name)
    new_name = ""
    message_args = message.content.split()
    for n in message_args[1:]:
        if(new_name!=''):
            new_name += " "
        new_name += n
    print("new_name="+new_name)
    write_param(message.server.id, "CMDR_"+message.author.id, new_name)
    put_message = ""
    if(current_name!=""):
        put_message = ", раніше я гадав, що ти CMDR "+current_name+", але тепер буду звати тебе CMDR "+new_name
    else:
        put_message = ", приємно познайомитись, CMDR "+new_name+"!"
    await client.send_message(message.channel,message.author.mention + put_message)


""" ================== сохранить имя командира ============================="""
async def on_translate(message):
    """Перевод фразы из игры"""
    args = message.content.split()
    print(len(args))
    print(args)
    in_word = ""
    for n in args[1:]:
        print('n='+n)
        print('in_word=' + in_word)
        if(in_word!=''):
            in_word += "%"
        in_word += n
        print('in_word2=' + in_word)
    new_ora = ora_data.ora_data()
    print('in_word='+in_word)
    result = new_ora.get_translate(in_word)
    if(result[0]['TRANSLATE']):
        print(result)
        await client.send_message(message.channel,message.author.mention + '```' + result[0]['TRANSLATE'] +'```')
    else:
        await client.send_message(message.channel,message.author.mention + ', співпадінь не знайдено.')

""" ================== сохранить префикс ============================="""
async def on_setprefix(message):
    message_args = message.content.split()
    print(len(message_args))
    if(len(message_args) != 2):
        await client.send_message(message.channel, message.author.mention + ', sorry, I can not determine which prefix you want to set.')
        return
    new_prefix = message_args[1]
    print("new_name="+new_prefix)
    config = read_config(message.server.id)
    config['prefix'] = str(new_prefix)
    print(config)
    save_config(message.server.id, config)
    await client.send_message(message.channel, message.author.mention + ', prefix set to `'+new_prefix+'`')

""" ================== ифнормация о миссиях за сегодня ============================="""
async def on_get_missions_on_day(message):
    print(message.channel.name)
    print(message.channel.id)
    if(message.channel.name.lower() != 'tactic_strategic'):
        return 0
    new_ora = ora_data.ora_data()
    m_missions = new_ora.get_missions_on_day(None)
    msg = ""
    for i, row in m_missions.items():
        msg = msg + str(row['CMDR']).ljust(10, ' ')[:10] + " " + \
                    str(row['FACTION']).ljust(25, ' ')[:25] + ' ' + \
                    str(row['COUNT_MISSIONS']).rjust(3, ' ')[:3] + ' ' + \
                    str(row['COUNT_MISSIONS2']).rjust(10, ' ')[:10] + ' ' + \
                    "{:,}".format((row['REWARD'] or 0)).rjust(10, ' ')[:10] + '\r\n'
    print(msg)
    await client.send_message(message.channel, '```'+msg+'```')


""" ================== ифнормация о наградах за сегодня ============================="""
async def on_get_bountys_on_day(message):
    print(message.channel.name)
    if(message.channel.name.lower() != 'tactic_strategic'):
        return 0
    new_ora = ora_data.ora_data()
    m_missions = new_ora.get_bountys_on_day(None)
    msg = ""
    for i, row in m_missions.items():
        msg = msg + str(row['CMDR']).ljust(10, ' ')[:10] + " " + \
                    str(row['FACTIONS']).ljust(35, ' ')[:35] + ' ' + \
                    "{:,}".format((row['AMOUNT'] or 0)).rjust(15, ' ')[:15] + '\r\n'
    print(msg)
    await client.send_message(message.channel, '```'+msg+'```')


""" ================== Список миссий по одному командиру ============================="""
async def on_get_my_missions(message):
    if(message.channel.name.lower() != 'uca_ukrainian_colonist'):
        return 0
    print(message.content)
    args = message.content.split()
    print(len(args))
    commander_name = ""

    commander_name = read_param(message.server.id, "CMDR_"+message.author.id)
    if(commander_name==""):
        await client.send_message(message.channel, message.author.mention + ", нажаль, я поки що так близько з тобою не знайомий. Але можемо познайомитися, якщо ти напишешь ""**!я твій нік**""")
        return
    print(commander_name)
    if(commander_name[0:2] == "<@"):
        commander_name = commander_name.replace("<@!", "").replace("<@", "")
        print('finding commander '+"CMDR_"+commander_name[:-1])
        commander_name = read_param(message.server.id, "CMDR_"+commander_name[:-1])
        if(commander_name==""):
            await client.send_message(message.channel, message.author.mention + ", нажаль, я щє не знайомий ц зим командиром. Але ми можемо познайомитися, якщо він напише ""!я його нік""")
            return
    print(commander_name)
    #await client.send_message(message.channel, message.author.mention + ', также известный как '+commander_name+', я тебя поцелую... потом... если захочешь...')
    new_ora = ora_data.ora_data()
    m_missions = new_ora.get_missions_on_day(commander_name)
    msg = ""
    for i, row in m_missions.items():
        msg = msg + str(row['FACTION']).ljust(25, ' ')[:25] + ' ' + \
                    str(row['COUNT_MISSIONS']).rjust(3, ' ')[:3] + ' ' + \
                    str(row['COUNT_MISSIONS2']).rjust(10, ' ')[:10] + ' ' + \
                    "{:,}".format((row['REWARD'] or 0)).rjust(10, ' ')[:10] + '\r\n'
    print(msg)
    if(msg):
        await client.send_message(message.channel, '```'+msg+'```')
    else:
        await client.send_message(message.channel, message.author.mention + ', нажаль сьогодні ти не зробив жодної місії...')

""" ================== Список полученных баунти по одному командиру ============================="""
async def on_get_my_bountys(message):
    if(message.channel.name.lower() != 'uca_ukrainian_colonist'):
        return 0
    print(message.content)
    args = message.content.split()
    print(len(args))
    commander_name = ""

    commander_name = read_param(message.server.id, "CMDR_"+message.author.id)
    if(commander_name==""):
        await client.send_message(message.channel, message.author.mention + ", нажаль, я поки що так близько з тобою не знайомий. Але можемо познайомитися, якщо ти напишешь ""**!я твій нік**""")
        return
    print(commander_name)
    if(commander_name[0:2] == "<@"):
        commander_name = commander_name.replace("<@!", "").replace("<@", "")
        print('finding commander '+"CMDR_"+commander_name[:-1])
        commander_name = read_param(message.server.id, "CMDR_"+commander_name[:-1])
        if(commander_name==""):
            await client.send_message(message.channel, message.author.mention + ", нажаль, я щє не знайомий ц зим командиром. Але ми можемо познайомитися, якщо він напише ""!я його нік""")
            return
    print(commander_name)
    new_ora = ora_data.ora_data()
    m_missions = new_ora.get_bountys_on_day(commander_name)
    msg = ""
    for i, row in m_missions.items():
        msg = msg + str(row['FACTIONS']).ljust(35, ' ')[:35] + ' ' + \
                    "{:,}".format((row['AMOUNT'] or 0)).rjust(15, ' ')[:15] + '\r\n'
    print(msg)
    if(msg):
        await client.send_message(message.channel, '```'+msg+'```')
    else:
        await client.send_message(message.channel, message.author.mention + ', нажаль сьогодні ти не здав жодної винагороди...')


""" ================== Список сбитых кораблей по одному командиру ============================="""
async def on_get_ship_kills_on_day(message):
    if(message.channel.name.lower() != 'uca_ukrainian_colonist'):
        return 0
    print(message.content)
    args = message.content.split()
    print(len(args))
    commander_name = ""

    commander_name = read_param(message.server.id, "CMDR_"+message.author.id)
    if(commander_name==""):
        await client.send_message(message.channel, message.author.mention + ", нажаль, я поки що так близько з тобою не знайомий. Але можемо познайомитися, якщо ти напишешь ""**!я твій нік**""")
        return
    print(commander_name)
    if(commander_name[0:2] == "<@"):
        commander_name = commander_name.replace("<@!", "").replace("<@", "")
        print('finding commander '+"CMDR_"+commander_name[:-1])
        commander_name = read_param(message.server.id, "CMDR_"+commander_name[:-1])
        if(commander_name==""):
            await client.send_message(message.channel, message.author.mention + ", нажаль, я щє не знайомий ц зим командиром. Але ми можемо познайомитися, якщо він напише ""!я його нік""")
            return
    print(commander_name)
    new_ora = ora_data.ora_data()
    m_missions = new_ora.get_ship_kills_on_day(commander_name)
    msg = ""
    for i, row in m_missions.items():
        msg = msg + str(row['TARGET']).ljust(25, ' ')[:25] + ' ' + \
                    "{:,}".format((row['TARGETCOUNT'] or 0)).rjust(15, ' ')[:15] + \
                    "{:,}".format((row['TOTALREWARD'] or 0)).rjust(15, ' ')[:15] + '\r\n'
    print(msg)
    if(msg):
        await client.send_message(message.channel, '```'+msg+'```')
    else:
        await client.send_message(message.channel, message.author.mention + ', нажаль сьогодні ти не знищив жодного корабля...')

""" ================== Пройденное расстояние ============================="""
async def on_get_distance_on_day(message):
    if(message.channel.name.lower() != 'uca_ukrainian_colonist'):
        return 0
    print(message.content)
    args = message.content.split()
    print(len(args))
    commander_name = ""

    commander_name = read_param(message.server.id, "CMDR_"+message.author.id)
    if(commander_name==""):
        await client.send_message(message.channel, message.author.mention + ", нажаль, я поки що так близько з тобою не знайомий. Але можемо познайомитися, якщо ти напишешь ""**!я твій нік**""")
        return
    print(commander_name)
    if(commander_name[0:2] == "<@"):
        commander_name = commander_name.replace("<@!", "").replace("<@", "")
        print('finding commander '+"CMDR_"+commander_name[:-1])
        commander_name = read_param(message.server.id, "CMDR_"+commander_name[:-1])
        if(commander_name==""):
            await client.send_message(message.channel, message.author.mention + ", нажаль, я щє не знайомий ц зим командиром. Але ми можемо познайомитися, якщо він напише ""!я його нік""")
            return
    print(commander_name)
    new_ora = ora_data.ora_data()
    m_missions = new_ora.get_distance_on_day(commander_name)
    msg = ""
    jumps = 0;
    for i, row in m_missions.items():
        jumps = row['JUMPSCOUNT']
        msg = msg + "Стрибків " + \
                    "{:,}".format((row['JUMPSCOUNT'] or 0)).rjust(6, ' ')[:6] + \
                    ", загальна відстань: " + \
                    "{:,}".format((row['JUMPDIST'] or 0)).rjust(10, ' ')[:10]+ \
                    ", використано пального: " + \
                    "{:,}".format((row['FUELUSED'] or 0)).rjust(10, ' ')[:10] + '\r\n'
    print(msg)
    if(jumps != 0):
        await client.send_message(message.channel, '```'+msg+'```')
    else:
        await client.send_message(message.channel, message.author.mention + ', нажаль сьогодні ти нікуди не стрибав...')


""" ================== эксперименты с многопотоковостью ============================="""
async def timer_status():
    print('timer_status')
    try:
        if client:
            if client.connected:
                print('set status')
                bot_game = discord.Game(name="Єдина Україна!", url="http://ed.dobrijzmej.org", type=0)
                await client.change_presence(game=bot_game)
    except Exception:
        print(traceback.format_exc())
    threading.Timer(5, timer_status).start()

#t_status = threading.Timer(5, timer_status)
#t_status.start()
#t_status.connect(reconnect=true)


client.run('********************************************')

