import os

from discord.ext import commands
from dotenv import load_dotenv
import requests
from formating.formating import *
from utils import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!a')


ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter cards include: Special player cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]

raw_text = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')
    await bot.change_presence(activity=discord.Game(name="a mejorar mazos"))


# @bot.command(name='t', help='Busca el registro de tabú de la carta pedida')
# async def look_for_taboo(ctx):

@bot.command(name='hhelp')
async def send_help(ctx):
    res = "¿Necesitas ayuda?: \n" \
          "" \
          "\n- !ahj [nombre] ~[subtitulo]~ ([extra]): Busca cartas en ArkhamDB.\n" \
          "[extra] puede contener ser lo siguiente: '0-5' nivel de la carta, " \
          "'G/B/R/M/S/N' la clase de la carta, P para permanente, U para único, E para excepcional.\n" \
          "Por ejemplo: \"!ahj Whisky (3S)\" devolverá el Whisky de Mosto Ácido de Supervivente de nivel 3. \n" \
          "\n- !ahm [nombre] ~[subtitulo]~: Busca cartas de encuentros (lugares, actos, escenarios, etc.) que no " \
          "sean cartas de jugador estándar. (¡Spoilers!) \n" \
          "\n- !ahd [numero]: Busca en ArkhamDB el mazo dado y lo muestra, tanto público como privado.\n" \
          "\n- !ahu [numero] [numero] Busca en ArkhamDB ambos mazos y muestra las mejoras realizadas en los mazos." \
          "Si mejoraste el mazo con ArkhamDB puedes también entregarle sólo el número del mazo más reciente." \
          ""
    await ctx.send(res)


@bot.command(name='hj')
async def look_for_player_card(ctx):
    skip = False
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = ah_player.copy()

    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext(c, sub_query)]

    if keyword_mode:
        r_cards = use_pc_keywords(r_cards, keyword_query)

    r_cards = search(query, r_cards)

    if len(r_cards) == 0:
        response = "No encontré ninguna carta"

    else:
        if r_cards[0]['name'] == "Debilidad básica aleatoria":
            skip = True
            response = "No encontré ninguna carta"

        elif r_cards[0]['type_code'] == "investigator":
            response = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = format_treachery_card(r_cards[0])
        else:
            response = format_player_card(r_cards[0])

        if len(r_cards) > 1 and not skip:
            response += "\n\n Encontré otras cartas más: \n%s" % list_rest(r_cards[1:min(4, len(r_cards))])
    await dev_send(showing, ctx, response)


@bot.command(name='hd')
async def look_for_deck(ctx, code: str):
    deck = find_deck(code)
    if not deck:
        response = "Mazo no encontrado"
        await ctx.send(response)
    else:
        deck_info = format_deck_cards(deck, ah_all_cards)
        embed = format_deck(deck, deck_info)
        response = "¡Mazo Encontrado!"
        await ctx.send(response, embed=embed)


# TODO: Armar los format_x...+
@bot.command(name='hm')
async def look_for_encounter(ctx, code: str):
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = ah_encounter.copy()
    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext_ec(c, sub_query)]
    if keyword_mode:
        r_cards = use_ec_keywords(r_cards, keyword_query)

    r_cards = search(query, r_cards)

    if len(r_cards) == 0:
        response = "No encontré ninguna carta"
    else:
        if r_cards[0]['type_code'] == "investigator":
            response = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = format_treachery_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            response = format_act_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            response = format_agenda_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            response = format_location_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            response = format_scenario_card(r_cards[0])

        else:
            response = format_player_card(r_cards[0])

        if len(r_cards) > 1:
            response += "\n\n Encontré otras cartas más: \n%s" % list_rest(r_cards[1:min(4, len(r_cards))])
    await dev_send(showing, ctx, response)

"""
@bot.command(name='s')
async def look_for_scenario_card(ctx, code: str):
    # Por scenario_card viene a ver acto/plan
    response = "Trabajando en algo nuevo c:"
    await dev_send(showing, ctx, response)

@bot.command(name='l')
async def look_for_location_card(ctx, code: str):
    query = ' '.join(ctx.message.content.split()[1:])
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    r_cards = search(query, ah_encounter)
    if sub_text_mode:
        r_cards = [c for c in r_cards if filter_by_subtext_ec(c, sub_query)]
    if keyword_mode:
        r_cards = use_ec_keywords(r_cards, keyword_query)

    # Lugares
    response = "Trabajando en algo nuevo c:"
    await dev_send(showing, ctx, response)
"""


async def dev_send(debug, ctx, string):
    if debug:
        await ctx.send("```%s```" % string)
    else:
        await ctx.send(string)


bot.run(TOKEN)
