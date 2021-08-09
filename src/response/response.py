import requests

from src.faq.formating import format_faq
from src.backs.search import resolve_back_search
from src.core.resolve import resolve_search
from src.core.search import card_search
from src.decks.deck import extract_deck_info
from src.decks.formating import format_deck
from src.decks.search import find_deck, search_for_upgrades
from src.e_cards.search import use_ec_keywords
from src.p_cards.search import use_pc_keywords
from src.rules.formating import format_rule
from src.rules.rules import search_for_rules

"""
    Aquí están todas las respuestas que tiene el bot, aquí es donde se hace la magia del bot, a partir de aquí
    el bot interactúa con los otros paquetes para hacer su magia.
"""

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()
ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]


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


def look_for_faq(query):
    """
    Given a query, returns a embed containing the faq of a card.
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
