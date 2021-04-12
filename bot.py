import os

import discord
from discord_slash import SlashCommand
import requests
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv

from FAQ.formating import format_faq
from backs.search import resolve_back_search
from core.formating import format_text
from rules.rules import search_for_concept
from rules.formating import format_concept
from core.resolve import resolve_search
from core.search import card_search
from decks.formating import format_deck
from decks.deck import extract_deck_info
from decks.search import search_for_upgrades, find_deck
from e_cards.search import use_ec_keywords, format_query_ec
from p_cards.search import use_pc_keywords, format_query_pc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!a')
slash = SlashCommand(bot, sync_commands=True)

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')
    await bot.change_presence(activity=discord.Game('hacer /'))


@bot.command(name='hhelp')
async def send_help_short(ctx):
    title = "¿Necesitas ayuda?"
    description = "Estos son los comandos de este Bot:"
    ahj = "``!ahj [nombre] ~[subtitulo]~ ([extra])``\n > Busca cartas de jugador y las muestra aquí."
    ahm = "``!ahm [nombre] ~[subtitulo]~ ([extra])``\n > Busca cartas de encuentros (lugares, actos, escenarios)."
    ahback = "``!ahback [nombre] ~[subtitulo]~ ([extra])``\n > Muestra la parte de atrás de ciertas cartas."
    ahd = "``!ahd [id]``\n > Busca en ArkhamDB el mazo dado."
    ahu = "``!ahu [id]``\n > Busca en ArkhamDB el mazo y calcula la mejora más reciente."
    ahp = "``!ahp [nombre] ~[subtitulo]~ ([extra])`` \n > Muestra los datos de la carta con las preguntas frecuentes." \
          " [WIP]"
    ahc = "``!ahr [nombre]`` \n > Busca reglas o palabras clave del manual del juego. [WIP]"
    ahhelp = "``!ahhelp``\n" \
             "> Devuelve la versión corta de la ayuda (esta). \n" \
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
          "**J**: Para cartas de jugador (Apoyos de Historia)."
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
          "Si el link es ``https://es.arkhamdb.com/deck/view/1320033`` entonces el id será ``1320033``. \n"
    ahu = "``!ahu [id]``\n " \
          ">>> Busca en ArkhamDB el historial de mazos y calcula la mejora según el mazo anterior en ArkhamDB."
    ahp = "``!ahp [nombre] ~[subtitulo]~ ([extra])`` \n > Muestra los datos de la carta con las preguntas frecuentes," \
          " interacciones extrañas y alguno que otro consejo para jugar esta carta. " \
          "\n [extra] Es el mismo que para ``!ahback`` y ``!ahm``"
    ahc = "``!ahr [nombre]`` \n > Busca reglas o palabras clave del manual del juego (o adaptados del manual, " \
          "porque mucho texto). "
    ahhelp = "``!ahhelp``\n" \
             "> Devuelve la versión corta de la ayuda." \
             "``!ahhelpme``\n" \
             "> Devuelve la versión larga de la ayuda (esta).\n"
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
async def look_for_upgrades(ctx, code):
    response, embed = search_for_upgrades(code, ah_player)
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


@bot.command(name='hr')
async def look_for_concept(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    search = search_for_concept(query)
    if search:
        embed = format_concept(search)
        await ctx.send("", embed=embed)
    else:
        await ctx.send("Hm... No encontré nada.")


@slash.slash(name="ah",
             description="Busca cartas de jugador en ArkhamDB.",
             options=[
                 create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
                 create_option(name="nivel", description="Nivel de la carta", option_type=4, required=False),
                 create_option(name="clase", description="Clase de la carta.", option_type=3, required=False,
                               choices=[
                                   create_choice(name="Guardián", value="G"),
                                   create_choice(name="Buscador", value="B"),
                                   create_choice(name="Rebelde", value="R"),
                                   create_choice(name="Místico", value="M"),
                                   create_choice(name="Superviviente", value="S"),
                                   create_choice(name="Neutral", value="N"),
                               ]),
                 create_option(name="extras", description="Extras", option_type=3, required=False,
                               choices=[
                                   create_choice(name="Permanente", value="P"),
                                   create_choice(name="Excepcional", value="E"),
                                   create_choice(name="Avanzada", value="A"),
                                   create_choice(name="Única", value="U"),
                                   create_choice(name="Característica", value="C"),
                               ]),
                 create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False),
             ])
async def ah_s(ctx, *args):
    query = format_query_pc(ctx.kwargs)
    r_cards = card_search(query, ah_player, use_pc_keywords)
    response, embed = resolve_search(r_cards)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahMazo",
             description="Muestra tu mazo de ArkhamDB.",
             options=[
                 create_option(name="id",
                               description="Código del mazo en ArkhamDB.",
                               option_type=4,
                               required=True)])
async def ahMazo_s(ctx, *args):
    deck = find_deck(ctx.kwargs.get('id'))
    if not deck:
        response = "Mazo no encontrado"
        await ctx.send(response)
    else:
        deck_info = extract_deck_info(deck, ah_all_cards)
        embed = format_deck(deck, deck_info)
        response = ""
        await ctx.send(response, embed=embed)


@slash.slash(name="ahMejora",
             description="Muestra la mejora de tu mazo de ArkhamDB",
             options=[
                 create_option(name="id",
                               description="Código del mazo en ArkhamDB.",
                               option_type=4,
                               required=True)])
async def ahMejora_s(ctx, *args):
    response, embed = search_for_upgrades(ctx.kwargs.get('id'), ah_player)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahe",
             description="Busca cartas de encuentros en ArkhamDB.",
             options=[
                 create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
                 create_option(name="tipo", description="Tipo de la carta.", option_type=3, required=False,
                               choices=[
                                   create_choice(name="Escenario", value="S"),
                                   create_choice(name="Acto", value="A"),
                                   create_choice(name="Plan", value="P"),
                                   create_choice(name="Traición", value="T"),
                                   create_choice(name="Enemigo", value="E"),
                                   create_choice(name="Lugares", value="L"),
                                   create_choice(name="Cartas de Jugador", value="J"),
                               ]),
                 create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False),
             ])
async def ahe_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    r_cards = card_search(query, ah_encounter, use_ec_keywords)
    response, embed = resolve_search(r_cards)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahFAQ",
             description="Busca FAQs en cartas.",
             options=[
                 create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
                 create_option(name="tipo", description="Tipo de la carta.", option_type=3, required=False,
                               choices=[
                                   create_choice(name="Escenario", value="S"),
                                   create_choice(name="Acto", value="A"),
                                   create_choice(name="Plan", value="P"),
                                   create_choice(name="Traición", value="T"),
                                   create_choice(name="Enemigo", value="E"),
                                   create_choice(name="Lugares", value="L"),
                                   create_choice(name="Cartas de Jugador", value="J"),
                               ]),
                 create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False),

             ])
async def ahfaq_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    r_cards = card_search(query, ah_all_cards, use_ec_keywords)
    if r_cards:
        embed = format_faq(r_cards[0])
        await ctx.send("", embed=embed)
    else:
        await ctx.send("No encontré la carta.")


@slash.slash(name="ahReglas",
             description="Busca Reglas/Conceptos del juego.",
             options=[create_option(name="regla",
                                    description="Nombre de la regla/concepto.",
                                    option_type=3,
                                    required=True)])
async def ahReglas_s(ctx, *args):
    query = ctx.kwargs.get('regla')
    search = search_for_concept(query)
    if search:
        embed = format_concept(search)
        await ctx.send("", embed=embed)
    else:
        await ctx.send("Hm... No encontré nada.")


@slash.slash(name="ahb",
             description="Busca las partes traseras de cartas.",
             options=[
                 create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
                 create_option(name="tipo", description="Tipo de la carta.", option_type=3, required=False,
                               choices=[
                                   create_choice(name="Escenario", value="S"),
                                   create_choice(name="Acto", value="A"),
                                   create_choice(name="Plan", value="P"),
                                   create_choice(name="Traición", value="T"),
                                   create_choice(name="Enemigo", value="E"),
                                   create_choice(name="Lugares", value="L"),
                                   create_choice(name="Cartas de Jugador", value="J"),
                               ]),
                 create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False),
             ])
async def ahback_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    f_cards = [c for c in ah_all_cards if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)
    response, embed = resolve_back_search(r_cards)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)

bot.run(TOKEN)
