import discord
import requests
import datetime
from keep_alive import host
import json
from discord.ext import commands
from PIL import Image

with open('champions.json', 'r', encoding="utf8") as f:
    data = json.load(f)

bot = commands.Bot(command_prefix='/', description="Bot creado por Dimitrix")

API_KEY = 'SOME_API_KEY'

challenger = "https://i.pinimg.com/originals/90/8f/95/908f95127caf7f739877f9f555807361.png"
gran_master = "https://www.eloboostroyal.es/assets/images/divisions/grandmaster.png"
master = "https://leagueof.hexania.com/assets/images/tier-icons/base-icons/Master_Emblem.png"
diamond = "https://i.pinimg.com/originals/6a/10/c7/6a10c7e84c9f4e4aa9412582d28f3fd2.png"
platinum = "https://i.pinimg.com/originals/d7/47/1e/d7471e2ef48175986e9b75b566f61408.png"
gold = "https://www.eloboostroyal.es/assets/images/divisions/gold.png"
silver = "https://static.wikia.nocookie.net/leagueoflegends/images/5/56/Season_2019_-_Silver_2.png/revision/latest/top-crop/width/300/height/300?cb=20181229234936"
bronze = "https://static.wikia.nocookie.net/leagueoflegends/images/8/81/Season_2019_-_Bronze_3.png/revision/latest/top-crop/width/300/height/300?cb=20181229234912"
iron = "https://www.eloboostroyal.es/assets/images/divisions/iron.png"


@bot.command()
async def version(contexto):
    embed = discord.Embed(title="- NUEVA VERSIÓN -", value=" ")
    embed.add_field(
        name="Contenido:",
        value=
        "1. Bugs corregidos del comando /rank, mas precisión y nueva información."
    )
    embed.set_thumbnail(
        url=
        "https://www.psdstamps.com/wp-content/uploads/2020/08/round-new-version-stamp-png.png"
    )
    await contexto.send(embed=embed)


@bot.command()
async def clash(contexto, jugador):
    api_load = f'https://la2.api.riotgames.com/lol/clash/v1/players/by-summoner/uuNyebGZB7t-EnjzPORCFVrjEnYUYnxCGRrUygAbDbDvUA?api_key={API_KEY}'


async def error(contexto):
  embed = discord.Embed(title="Jugador no encontrado.",
                        description="Por favor, vuelve a intentar.",
                        color=discord.Color.red())
  embed.set_thumbnail(
      url=
      "https://media.tenor.com/images/17957c943fb8dac6b816d01730980cf4/tenor.gif"
  )
  await contexto.send(embed=embed)

def icon_founded(name_pj):
    name_pj = name_pj.lower()
    url = f"http://ddragon.leagueoflegends.com/cdn/11.8.1/img/champion/{name_pj.capitalize()}.png"

    return url

@bot.command()
async def champ(contexto, playername, championname):
  try:
    summoner_id = summoner(playername)
    id_sum = summoner_id[0]
    champ = champ_stats(id_sum, championname)
    icon = champ[0]
    points = champ[1]
    mastery = champ[2]
    embed = discord.Embed(title=f"Maestria {championname} de {playername}",
                          description=f"-------------",
                          color=discord.Color.blue())
    embed.add_field(name="Estadísticas", value=f"Puntos:{points}")
    embed.add_field(name="Nivel de Maestria", value=f"Lvl:{mastery}")
    embed.set_image(icon)
    await contexto.send(embed=embed)
  except:
    await error(contexto)

def iteracion_champ(cantidad, champ_list, mains_list, mains_point_list):

    for champ in champ_list[0:cantidad]:
        mains_list.append(champ['championId'])
        mains_point_list.append(champ['championPoints'])

    return mains_list, mains_point_list


def champ_stats(id_sum, multiple=True, championname=""):

    url_champ = f"https://la2.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id_sum}?api_key={API_KEY}"
    request_champs = requests.get(url_champ)
    champs_list_json = request_champs.json()

    mains = []
    mains_name = []
    mains_points = []
    first = True

    if multiple is False:
        get_main = iteracion_champ(None, champs_list_json, mains, mains_points)
        mains = get_main[0]
        mains_points = get_main[1]
    else:
        get_mains = iteracion_champ(3, champs_list_json, mains, mains_points)
        mains = get_mains[0]
        mains_points = get_mains[1]


    for champion in mains:
        for champ in data['data']:
            if str(champion) == data['data'][champ]['key']:
                name = data['data'][champ]['name']
                mains_name.append(name)
                if first:
                    url = icon_founded(name)
                    first = False
                break

    return mains_name, mains_points, url


def summoner(nombre):

    print("\n----\nFuncion SUMMONER, {}".format(nombre))
    summoner_id = f"https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nombre}?api_key={API_KEY}"
    print("\n-----\nlink: {}".format(summoner_id))
    perfil_load = requests.get(summoner_id)
    perfil_json = perfil_load.json()
    nivel = perfil_json["summonerLevel"]
    id_sum = perfil_json["id"]
    return id_sum, nivel


def stats_summoner(id_sum, mode):

  try:

    # Obtenemos los datos con la API y la APIKEY.
    stats_summoner = f'https://la2.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_sum}?api_key={API_KEY}'
    data_lol = requests.get(stats_summoner)
    data_lol_loaded = data_lol.json()

    #Algoritmo para detectar precisamente si las estadisticas son de SOloDUO o Flex.
    if mode == "solo":
        mode = "Solo/Dúo"
        if data_lol_loaded[0]['queueType'] == "RANKED_SOLO_5x5":
            info = data_lol_loaded[0]
        else:
            info = data_lol_loaded[1]
    else:
        if data_lol_loaded[0]['queueType'] == "RANKED_FLEX_SR":
            info = data_lol_loaded[0]
        else:
            info = data_lol_loaded[1]

    wins = info["wins"]
    losses = info["losses"]
    winratio = (wins / (wins + losses)) * 100
    tier = info["tier"]
    rank = info["rank"]
    lp = info["leaguePoints"]
    racha = info["hotStreak"]

    return wins, losses, winratio, tier, rank, lp, racha

  except:
    return "Error", "Error", "Error", "Error", "Error", "Error", "Error"


@bot.command()
async def ayuda(contexto):
    embed = discord.Embed(title="- Hola, soy el robot de Dimitrix.",
                          value="Fui creado para diversos usos.",
                          color=discord.Color.blue())
    embed.add_field(
        name="Comandos:",
        value="Estadisticas rankeds LOL: /rank USUARIO MODO (en modo va "
        'solo'
        " o "
        'flex'
        "\nTambien se la temperatura de las ciudades: /temperatura CIUDAD")
    embed.set_image(
        url=
        "https://lh3.googleusercontent.com/proxy/Qhtf0_6iSdErvF6tZSMEaAKo1gDC5RZI5M1d_zJjmrAaTHDoyytRBk5_Iivr5o-sU9k3GUvx7egQ6tBpL3eHKGFePKZd4a3f8viTH8cFtE-_WGDDNqBHas5ufdlF2d2LHQ"
    )
    await contexto.send(embed=embed)


@bot.command()
async def rank(contexto, modo, *, nombre):
  nombre = str(nombre)
  try:
    if modo == "solo":
        print("\n----\nFuncion rank, {}".format(nombre))
        await contexto.send("Buscando a: {}".format(nombre))
        await get_info(contexto, "solo", nombre)
    elif modo == "flex":
        await contexto.send("Buscando a: {}".format(nombre))
        await get_info(contexto, "flex", nombre)
    else:
        await contexto.send(f"El comando es: /rank MODO JUGADOR")
  except:
    await error(contexto)

async def get_info(contexto, mode, nombre):
    try:
        print("\n----\nFuncion get info, {}".format(nombre))
        summoner_profile = summoner(nombre)
        print("Debugeado")
        nivel = summoner_profile[1]
        print("Debugeado")
        id_sum = summoner_profile[0]
        print("Debugeado")
        summoner_stats_load = stats_summoner(id_sum, mode)
        print("Debugeado 123131123")
        wins = summoner_stats_load[0]
        print("Debugeado")
        losses = summoner_stats_load[1]
        print("Debugeado")
        winratio = summoner_stats_load[2]
        print("Debugeado")
        tier = summoner_stats_load[3]
        rank = summoner_stats_load[4]
        lp = summoner_stats_load[5]
        print("Debugeado")
        racha = summoner_stats_load[6]
        if racha:
            racha = "Está en racha"
        else:
            racha = "No está en racha."
        main = champ_stats(id_sum)
        mains_name = main[0]
        mains_points = main[1]
        main_1 = mains_name[0]
        main_2 = mains_name[1]
        main_3 = mains_name[2]
        url = main[2]
        main_1_Points = mains_points[0]
        main_2_Points = mains_points[1]
        main_3_Points = mains_points[2]
        print("\n------------\nDEBUGGING\n")
        print(rank)
        print(url)
        print(main)
        print(summoner_stats_load)
        print(summoner_profile)


    except:
        await error(contexto)
    else:
        marco = ""
        if tier == "CHALLENGER":
            marco = challenger
            color_msg = discord.Color.yellow()
        if tier == "GRAN MASTER":
            marco = gran_master
            color_msg = discord.Color.blue()
        if tier == "MASTER":
            marco = master
            color_msg = discord.Color.purple()
        if tier == "DIAMOND":
            marco = diamond
            color_msg = discord.Color.blue()
        if tier == "PLATINUM":
            marco = platinum
            color_msg = discord.Color.green()
        if tier == "GOLD":
            marco = gold
            color_msg = discord.Color.orange()
        if tier == "SILVER":
            marco = silver
            color_msg = discord.Color.light_grey()
        if tier == "BRONZE":
            marco = bronze
            color_msg = discord.Color.dark_orange()
        if tier == "IRON":
            marco = iron
            color_msg = discord.Color.dark_grey()

        embed = discord.Embed(
            title=f"[ {mode.upper()}]- Perfil de invocador: {nombre.upper()}",
            description=f"\nNivel:{nivel}\nFecha: {hora_actual}",
            color=color_msg)
        embed.add_field(
            name="******** ESTADÍSTICAS ********",
            value="-------------------------------------------------")
        embed.add_field(name="Ganadas y Perdidas:",
                        value=f"Wins: {wins} \nLosses: {losses}")
        embed.add_field(name="Ratio de ganadas:",
                        value=f"Ganó el {int(winratio)}%.")
        embed.add_field(name="Posicion actual:", value=f"{tier} {rank}.")
        embed.add_field(name="Puntos de Liga", value=f"{lp} League Points.")
        embed.add_field(name="¿Racha?", value=f"{racha}")
        embed.set_thumbnail(url=marco)
        embed.set_image(url=url)
        embed.add_field(
            name="Top Maestrías:",
            value=
            f"1 - [ {main_1} Puntos: {main_1_Points}]\n2 - [{main_2} Puntos: {main_2_Points}]\n3 - [{main_3} Puntos: {main_3_Points}]"
        )
        await contexto.send(embed=embed)


@bot.command()
async def miembros(contexto):
    await contexto.send("a")


@bot.command()
async def saludar(contexto):
    await contexto.send('Hola, soy el Robot creado por Dimitrix.')


@bot.command()
async def programado(contexto):
    await contexto.send('Estoy programado en Python.')


@bot.command()
async def temperatura(contexto, ciudad):
    api_key = '401af7d7340cc7b606ec51fb8be0afed'
    es = "es"
    api_loaded = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang={es}'
    weather_data = requests.get(api_loaded)
    temperatura_json = weather_data.json()
    print(temperatura_json)
    if temperatura_json["cod"] != "404":
        estado = temperatura_json["weather"]
        temperatura_cargada = temperatura_json["main"]
        temperatura_ciudad = temperatura_cargada["temp"]
        estado_cielo = estado[0]['description']
        temperatura_ciudad_celsius = temperatura_ciudad - 273.15
        hora_actual = datetime.date.today()
        embed = discord.Embed(
            title=f"- Temperatura {ciudad.upper()} -\n",
            color=discord.Color.random(),
            description=
            " | Temperatura: {} Grados Celsius. |\n| Fecha: {} |\n| Creado por Dimitrix. |"
            .format(int(temperatura_ciudad_celsius), hora_actual))
        embed.set_thumbnail(
            url=
            "https://c0.klipartz.com/pngpicture/266/445/gratis-png-alat-clima-registrador-de-datos-de-cambio-climatico-el-clima.png"
        )
        embed.add_field(name="Estado del Cielo: ", value=estado_cielo.upper())
        await contexto.send(embed=embed)
    else:
        embed = discord.Embed(title="- Error -",
                              description="Esa ciudad no existe.")
        embed.set_thumbnail(
            url=
            "https://www.kindpng.com/picc/m/164-1646889_error-png-page-something-went-wrong-png-transparent.png"
        )
        await contexto.send(embed=embed)


@bot.event  ## mensaje de ON
async def on_ready():
    await bot.change_presence(activity=discord.player(
        name="ROBOT", url="http://www.twitch.tv/accountname"))
    print('Bot listo para usar.')

    ## prendiendo el bot


host()
bot.run('SOME_DISCORD_PRIVATE_KEYS')
