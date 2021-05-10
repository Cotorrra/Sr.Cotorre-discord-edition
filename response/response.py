import discord
import requests
from discord_slash.utils.manage_commands import create_option, create_choice

from FAQ.formating import format_faq
from backs.search import resolve_back_search
from core.resolve import resolve_search
from core.search import card_search
from decks.deck import extract_deck_info
from decks.formating import format_deck
from decks.search import find_deck, search_for_upgrades
from e_cards.search import use_ec_keywords
from p_cards.search import use_pc_keywords
from rules.formating import format_rule
from rules.rules import search_for_rules

"""
    Aquí están todas las respuestas que tiene el bot, aquí es donde se hace la magia del bot, a partir de aquí
    el bot interactúa con los otros paquetes para hacer su magia.
"""

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()
ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]


def help_short():
    """
    Returns a Discord.Embed that contains the short help text.
    :return: u Discord.Embed
    """
    title = "¿Necesitas ayuda?"
    description = "Estos son los comandos de este Bot:"
    ahj = "``!ahj [nombre] ~[subtitulo]~ ([extra])``\n > Busca cartas de jugador y las muestra aquí."
    ahm = "``!ahm [nombre] ~[subtitulo]~ ([extra])``\n > Busca cartas de encuentros (lugares, actos, escenarios)."
    ahback = "``!ahback [nombre] ~[subtitulo]~ ([extra])``\n > Muestra la parte de atrás de ciertas cartas."
    ahd = "``!ahd [id]``\n > Busca en ArkhamDB el mazo dado."
    ahu = "``!ahu [id]``\n > Busca en ArkhamDB el mazo y calcula la mejora más reciente."
    ahp = "``!ahp [nombre] ~[subtitulo]~ ([extra])`` \n > Muestra los datos de la carta con las preguntas frecuentes." \
          " [WIP]"
    ahr = "``!ahr [nombre]`` \n > Busca reglas o palabras clave del manual del juego. [WIP]"
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
    embed.add_field(name="Preguntas frecuentes:", value=ahp, inline=False)
    embed.add_field(name="Reglas:", value=ahr, inline=False)
    embed.add_field(name="Ayuda:", value=ahhelp, inline=False)
    return "", embed


def help_long():
    """
    Returns a Discord.Embed that contains the LONG help text.
    :return: a Discord.Embed
    """
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
    ahr = "``!ahr [nombre]`` \n > Busca reglas o palabras clave del manual del juego (o adaptados del manual, " \
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
    embed.add_field(name="Preguntas frecuentes:", value=ahp, inline=False)
    embed.add_field(name="Reglas:", value=ahr, inline=False)
    embed.add_field(name="Ayuda:", value=ahhelp, inline=False)
    embed.set_footer(text=footnote)
    return "", embed


def look_for_player_card(query: str):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :param cards: The cards to search from
    :param keyword_fun: A function that filters cards given the keywords in (TYPE)
    :return: a Discord.Embed
    """
    r_cards = card_search(query, ah_player, use_pc_keywords)
    embed = resolve_search(r_cards)
    if embed:
        return "", embed
    else:
        return "No se encontró la carta.", False


def look_for_mythos_card(query: str):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a mythos card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = card_search(query, ah_encounter, use_ec_keywords)
    embed = resolve_search(r_cards)
    if embed:
        response = ""
    else:
        response = "No se encontró la carta."

    return response, embed


def look_for_card_back(query: str):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a back of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    f_cards = [c for c in ah_all_cards if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)
    embed = resolve_back_search(r_cards)
    if embed:
        response = ""
    else:
        response = "No se encontró la carta."

    return response, embed


def look_for_deck(code, deck_type):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed that contains the information of that deck.
    :param deck_type:
    :param code: ArkhamDB ID
    :return:
    """
    deck = find_deck(code, deck_type)
    if not deck:
        response = "Mazo no encontrado"
        embed = False
    else:
        deck_info = extract_deck_info(deck, ah_all_cards)
        embed = format_deck(deck, deck_info)
        response = ""
    return response, embed


def look_for_upgrades(code, deck_type):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed the contains the upgrade information of that deck if any.
    :param deck_type:
    :param code: ArkhamDB ID
    :return:
    """
    return search_for_upgrades(code, ah_player, deck_type)


def look_for_faq(query) -> discord.Embed:
    """
    Given a query, returns a embed containing the FAQ of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return:
    """
    r_cards = card_search(query, ah_all_cards, use_ec_keywords)
    if r_cards:
        embed = format_faq(r_cards[0])
        response = ""
    else:
        response = "No se encontró la carta."
        embed = False
    return response, embed


def look_for_rule(query):
    """
    Given a query, returns a embed containing a rule of the game
    :param query:  A query string.
    :return:
    """
    search = search_for_rules(query)
    if search:
        embed = format_rule(search)
        response = ""
    else:
        embed = False
        response = "No se encontró la regla."
    return response, embed


def player_card_slash_options():
    """
    Returns the slash command options for player cards.
    :return:
    """
    return [create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
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
            create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False)]


def deck_slash_options():
    """
    Returns the slash command options for decks.
    :return:
    """
    return [create_option(name="id",
                          description="Código del mazo en ArkhamDB.",
                          option_type=4,
                          required=True),
            create_option(name="tipo", description="Tipo de Mazo", option_type=3, required=False,
                          choices=[
                              create_choice(name="Público", value="decklist"),
                              create_choice(name="Privado", value="deck"),
                          ]),
            ]


def general_card_slash_options():
    """
    Returns the slash command options for general cards.
    :return:
    """
    return [create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
            create_option(name="tipo", description="Tipo de la carta.", option_type=3, required=False,
                          choices=[
                              create_choice(name="Escenario", value="S"),
                              create_choice(name="Acto", value="A"),
                              create_choice(name="Plan", value="P"),
                              create_choice(name="Traición", value="T"),
                              create_choice(name="Enemigo", value="E"),
                              create_choice(name="Lugares", value="L"),
                              create_choice(name="Cartas de Jugador", value="J"),
                              create_choice(name="Mitos (Encuentros)", value="M"),
                          ]),
            create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False)]


def rules_slash_options():
    """
    Returns the slash command options rules.
    :return:
    """
    return [create_option(name="regla",
                          description="Nombre de la regla/concepto.",
                          option_type=3,
                          required=True)]
