import urllib.request
import json
import main

async def on_find_station(message):
    print(message.content)
    args = message.content.split()
    print(len(args))
    system_name = ""
    for n in args[1:]:
        if(system_name!=''):
            system_name += "+"
        system_name += n
    url = "https://eddb.io/system/search?system[name]="+system_name+"&expand=stations&system[version]=2"
    print("send query "+url)
    result = urllib.request.urlopen(url).read()
    print(result.decode('ascii'))

    stantion_list = json.loads(result.decode('ascii'))

    await main.client.send_message(message.channel, message.author.mention + ", знайдено " + len(stantion_list) + " станцій ")

    """result = json.loads(result.decode('ascii'))
    if(result['msgnum'] == 100):
        s_system = '[інформація закрита пілотом]'
        if(not result['system'] is None):
            s_system = result['system']
        s_date = '[інформація закрита пілотом]'
        if (not result['date'] is None):
            s_date = result['date']
        await client.send_message(message.channel, message.author.mention+", останній раз пілота бачили "+s_date+" у системі "+s_system)
    else:
        await client.send_message(message.channel, message.author.mention+", нажаль, при пошуку пілота сталася помилка: "+result['msg'])
"""