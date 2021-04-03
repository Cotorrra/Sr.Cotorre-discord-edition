import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

from FAQ.formating import format_faq
from backs.search import resolve_back_search
from core.resolve import resolve_search
from core.search import card_search
from decks.formating import format_deck
from decks.deck import extract_deck_info
from decks.search import search_for_upgrades, find_deck
from e_cards.search import use_ec_keywords
from p_cards.search import use_pc_keywords

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!a')

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='tus Miedos'))


@bot.command(name='hhelp')
async def send_help_short(ctx):
    title = "¿Necesitas ayuda?"
    description = "Estos son los comandos de este Bot:"
    ahj = "``!ahj [nombre] ~[subtitulo]~ ([extra])``\n > Busca cartas de jugador y las muestra aquí."
    ahm = "``!ahm [nombre] ~[subtitulo]~ ([extra])``\n > Busca cartas de encuentros (lugares, actos, escenarios)."
    ahback = "``!ahback [nombre] ~[subtitulo]~ ([extra])``\n > Muestra la parte de atrás de ciertas cartas."
    ahd = "``!ahd [id]``\n > Busca en ArkhamDB el mazo dado."
    ahu = "``!ahu [id]``\n > Busca en ArkhamDB el mazo y calcula la mejora más reciente."
    ahhelp = "``!ahhelp``\n" \
             "> Devuelve la versión corta de la ayuda (esta)." \
             "``!ahhelpme``\n" \
             "> Devuelve la versión larga de la ayuda."
    embed = discord.Embed(title=title, description=description)
    embed.add_field(name="Cartas de Jugador:", value=ahj, inline=False)
    embed.add_field(name="Cartas de Encuentros:", value=ahm, inline=False)
    embed.add_field(name="Partes traseras de Cartas:", value=ahback, inline=False)
    embed.add_field(name="Mazos de ArkhamDB:", value=ahd, inline=False)
    embed.add_field(name="Mejoras de Mazos de ArkhamDB:", value=ahu, inline=False)
    embed.add_field(name="Ayuda:", value=ahhelp, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='hhelpme')
async def send_help(ctx):
    title = "¿Necesitas ayuda?"
    description = "Estos son los comandos de este Bot:"
    ahj = "``!ahj [nombre] ~[subtitulo]~ ([extra])``\n" \
          ">>> Busca cartas en ArkhamDB y las muestra aquí.\n" \
          "``[extra]`` puede ser cualquier combinación de lo siguiente: \n" \
          "**0-5** para el Nivel\n" \
          "**G**, **B**, **R**, **M**, **S** y **N** para la Clase.\n" \
          "**P**: para cartas Permanentes\n" \
          "**U**: para cartas Únicas\n" \
          "**E**: para cartas Excepcionales\n" \
          "**C**: para cartas Características\n" \
          "**A**: para cartas Avanzadas de los investigadores paralelos.\n" \
          "Ejemplo: \n" \
          "``!ahj Whisky (3S)`` devolverá: https://es.arkhamdb.com/card/05191\n" \
          "``!ahj Solución ~Acido~`` devolverá: https://es.arkhamdb.com/card/02263"
    ahm = "``!ahm [nombre] ~[subtitulo]~ ([extra])``\n" \
          ">>> Busca cartas de encuentros (lugares, actos, escenarios, " \
          "etc.) que no sean cartas de jugador estándar. (¡Ojo con los Spoilers!) \n" \
          "``[extra]`` puede contener lo siguiente:\n " \
          "**S**: para Escenario\n" \
          "**A**: para Actos\n" \
          "**P**: para Planes\n" \
          "**T**: para Traiciones\n" \
          "**E**: para Enemigos\n" \
          "**L**: Lugares\n" \
          "**J**: Para cartas de jugador."
    ahback = "``!ahback [nombre] ~[subtitulo]~ ([extra])``\n" \
             ">>> Muestra la parte de atrás de ciertas cartas. \n" \
             "``[extra]`` puede contener lo siguiente:\n" \
             "**S**: para Escenarios\n" \
             "**A**: para Actos\n" \
             "**P**: para Planes\n" \
             "**T**: para Traiciones\n" \
             "**E**: para Enemigos\n" \
             "**L**: para Lugares\n" \
             "**J**: para Cartas de jugador de encuentros."
    ahd = "``!ahd [id]``\n" \
          ">>> Busca en ArkhamDB el mazo dado y lo muestra, si es público o privado. \n" \
          "Si el link es ``https://es.arkhamdb.com/deck/view/1320033`` entonces su id será ``1320033``."
    ahu = "``!ahu [id]``\n " \
          ">>> Busca en ArkhamDB el historial de mazos y calcula la mejora según el mazo anterior en ArkhamDB."
    ahhelp = "``!ahhelp``\n" \
             "> Devuelve la versión corta de la ayuda." \
             "``!ahhelpme``\n" \
             "> Devuelve la versión larga de la ayuda (esta)."
    footnote = "El Sr. \"Co-Torre\"™ es desarrollado por Cotorra."
    embed = discord.Embed(title=title, description=description)
    embed.add_field(name="Cartas de Jugador:", value=ahj, inline=False)
    embed.add_field(name="Cartas de Encuentros:", value=ahm, inline=False)
    embed.add_field(name="Partes traseras de Cartas:", value=ahback, inline=False)
    embed.add_field(name="Mazos de ArkhamDB:", value=ahd, inline=False)
    embed.add_field(name="Mejoras de Mazos de ArkhamDB:", value=ahu, inline=False)
    embed.add_field(name="Ayuda:", value=ahhelp, inline=False)

    embed.set_footer(text=footnote)
    await ctx.send(embed=embed)


@bot.command(name='hback')
async def look_for_card_back(ctx):
    query = ' '.join(ctx.message.content.split()[1:])

    f_cards = [c for c in ah_all_cards if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)

    response, embed = resolve_back_search(r_cards)

    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hj')
async def look_for_player_card(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    r_cards = card_search(query, ah_player, use_pc_keywords)
    response, embed = resolve_search(r_cards)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hd')
async def look_for_deck(ctx, code: str):
    deck = find_deck(code)
    if not deck:
        response = "Mazo no encontrado"
        await ctx.send(response)
    else:
        deck_info = extract_deck_info(deck, ah_all_cards)
        embed = format_deck(deck, deck_info)
        response = ""
        await ctx.send(response, embed=embed)


@bot.command(name='hm')
async def look_for_encounter(ctx, code: str):
    query = ' '.join(ctx.message.content.split()[1:])
    r_cards = card_search(query, ah_encounter, use_ec_keywords)
    response, embed = resolve_search(r_cards)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


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
@bot.command(name='hu')
async def look_for_upgrades(ctx):
    query = ' '.join(ctx.message.content.split()[1:])

    response, embed = search_for_upgrades(query, ah_player)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hp')
async def look_for_faq(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    r_cards = card_search(query, ah_all_cards, use_ec_keywords)
    if r_cards:
        embed = format_faq(r_cards[0])
        await ctx.send("", embed=embed)
    else:
        await ctx.send("No encontré la carta.")


@bot.command(name='hc')
async def look_for_concept(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    search = search_for_concept(query)
    if search:
        embed = format_concept(search)
        await ctx.send("", embed=embed)
    else:
        await ctx.send("Hm... No encontré nada.")

bot.run(TOKEN)
