"""
    Response module.
    Handles the searches from the bot commands.
"""
import random

from src.api_interaction.cycle import cycle
from src.api_interaction.preview import preview
from src.api_interaction.timings import timings
from src.core.cardsDB import cards
from src.core.formating import create_embed
from src.core.translator import lang
from src.api_interaction.errata import errata
from src.backs.search import resolve_back_search
from src.response.resolve import resolve_search
from src.core.search import card_search
from src.decks.deck import extract_deck_info, check_upgrade_rules
from src.decks.formating import format_deck, format_upgraded_deck, format_list_of_cards
from src.decks.search import find_deck, find_former_deck
from src.e_cards.search import use_ec_keywords
from src.p_cards.search import use_pc_keywords
from src.api_interaction.taboo import taboo
from src.api_interaction.tarot import tarot, format_tarot


def refresh_cards():
    """Refreshes the cards from ArkhamDB"""
    cards.refresh()
    return True


def refresh_api_data():
    cycle.reload_cycles()
    errata.reload_errata()
    lang.reload_language()
    preview.reload_preview()
    taboo.reload_taboo()
    tarot.reload_tarot()
    timings.reload_timings()
    return True


def look_for_player_card(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords)
    embed = resolve_search(r_cards)

    if embed:
        return embed, False

    return create_embed(lang.locale('card_not_found')), True


def look_for_mythos_card(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a mythos card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = card_search(query, cards.get_e_cards(), use_ec_keywords)
    embed = resolve_search(r_cards)
    if embed:
        return embed, False

    return create_embed(lang.locale('card_not_found')), True


def look_for_card_back(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a back of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    f_cards = [c for c in cards.get_all_cards() if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)
    embed = resolve_back_search(r_cards)
    if embed:
        return embed, False

    return create_embed(lang.locale('card_not_found')), True


def look_for_deck(code, deck_type):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed that contains the information of that deck.
    :param deck_type:
    :param code: ArkhamDB ID
    :return:
    """
    deck = find_deck(code, deck_type)
    if deck:
        deck_info = extract_deck_info(deck, cards.get_all_cards())
        embed = format_deck(deck, deck_info)
        return embed, False

    return create_embed(lang.locale('deck_not_found')), True


def look_for_upgrades(code, deck_mode):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed that
    contains the upgrade information of that deck if any.
    :param code: ArkhamDB ID
    :param deck_mode: if it is a decklist or a privatedeck
    :return:
    """
    deck1 = find_deck(code, deck_mode)
    deck2 = find_former_deck(code, deck_mode)
    if not deck1:
        return create_embed(lang.locale('deck_not_found')), True
    elif not deck2:
        return create_embed(lang.locale('upgrade_not_found')), True

    info = check_upgrade_rules(deck2, deck1, cards.get_all_cards())
    return format_upgraded_deck(deck1, info), False


def look_for_faq(query):
    """
    Given a query, returns a embed containing the faq of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return:
    """
    # r_cards = card_search(query, cards.get_all_cards(), use_ec_keywords)
    # if r_cards:
    #    embed = format_faq(r_cards[0])
    # else:
    #   embed = create_embed(lang.locale('card_not_found'), "", {})
    # return embed
    ...


def look_for_rule(query):
    """
    Given a query, returns an embed containing a rule of the game
    :param query:  A query string.
    :return:
    """
    # search = search_for_rules(query)
    # if search:
    #    embed = format_rule(search)
    # else:
    #    embed = create_embed(lang.locale('card_not_found'), "", {})
    # return embed


def look_for_tarot(query):
    """
    Given a query, returns a embed containing a tarot card of the game.
    If the query is empty, returns a random tarot card.
    :param query:  A query string.
    :return:
    """
    search = tarot.search_for_tarot(query)
    if search:
        return format_tarot(search), False

    return create_embed(lang.locale('card_not_found')), True


def look_for_list_of_cards(query):
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords)
    result = [(c, 1) for c in r_cards[:10]]
    text = ">>> " + format_list_of_cards(result, sort=False)
    title = f"{lang.locale('ahList_title')} {len(result)}"
    embed = create_embed(title, text)
    if r_cards:
        return embed, False
    else:
        create_embed(lang.locale('card_not_found')), True


def look_for_random_player_card(query):
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords, allow_empty=True)
    card = random.choice(r_cards)
    embed = resolve_search([card])
    if embed:
        return embed, False
    else:
        create_embed(lang.locale('card_not_found')), True


def look_for_framework(query):
    embed = timings.find_formated_timing(query)
    return embed, False


def look_for_preview_player_card(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = [c for c in preview.get_preview_data() if c['code'] == query['card']]
    embed = resolve_search(r_cards)

    if embed:
        return embed, False

    return create_embed(lang.locale('card_not_found')), True
