import random

from src.api_interaction.preview import preview
from src.api_interaction.tarot import format_tarot, tarot
from src.api_interaction.timings import timings
from src.backs.search import resolve_back_search
from src.core.cards_db import cards
from src.core.formatting import create_embed
from src.core.search import card_search
from src.core.translator import locale as _
from src.decks.deck import check_upgrade_rules, extract_deck_info
from src.decks.formatting import format_deck, format_list_of_cards, format_upgraded_deck
from src.decks.search import find_deck, find_former_deck
from src.e_cards.search import use_ec_keywords
from src.p_cards.search import use_pc_keywords
from src.response.resolve import resolve_customizable, resolve_search
from src.who.who import resolve_search_who


def refresh_cards():
    """Refreshes the cards from ArkhamDB"""
    cards.refresh()
    return True


def look_for_player_card(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords)
    if not r_cards:
        return create_embed(_("card_not_found")), True

    embed = resolve_search(r_cards)
    return embed, False


def look_for_mythos_card(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a mythos card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = card_search(query, cards.get_e_cards(), use_ec_keywords)
    if not r_cards:
        return create_embed(_("card_not_found")), True

    embed = resolve_search(r_cards)
    return embed, False


def look_for_card_back(query: dict):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a back of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    f_cards = [c for c in cards.get_all_cards() if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)
    if not r_cards:
        return create_embed(_("card_not_found")), True

    embed = resolve_back_search(r_cards)
    return embed, False


def look_for_deck(code, deck_type):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed that contains the information of that deck.
    :param deck_type:
    :param code: ArkhamDB ID
    :return:
    """
    deck = find_deck(code, deck_type)
    if not deck:
        return create_embed(_("deck_not_found")), True

    deck_info = extract_deck_info(deck, cards.get_all_cards())
    embed = format_deck(deck, deck_info)
    return embed, False


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
        return create_embed(_("deck_not_found")), True
    if not deck2:
        return create_embed(_("upgrade_not_found")), True

    info = check_upgrade_rules(deck2, deck1, cards.get_all_cards())
    return format_upgraded_deck(deck1, info), False


def look_for_tarot(query):
    """
    Given a query, returns a embed containing a tarot card of the game.
    If the query is empty, returns a random tarot card.
    Arguments:
        query --  A query string.
    Returns:
        A Discord.Embed with the tarot card of the query
    """
    search = tarot.search_for_tarot(query)
    if not search:
        return create_embed(_("card_not_found")), True

    return format_tarot(search), False


def look_for_list_of_cards(query):
    """Given a query, returns a list of cards that match the query.

    Arguments:
        query -- A query string.

    Returns:
        A Discord.Embed with the list of cards that match the query.
    """
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords)
    if not r_cards:
        return create_embed(_("card_not_found")), True

    result = [(c, 1) for c in r_cards[:10]]
    text = ">>> " + format_list_of_cards(result, sort=False)
    title = f"{_('ahList_title')} {len(result)}"
    embed = create_embed(title, text)
    return embed, False


def look_for_random_player_card(query):
    """Given a query, returns a embed containing a random card.

    Arguments:
        query -- A query string. To filter the random card.

    Returns:
        A Discord.Embed with the random card of the query
    """
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords, allow_empty=True)
    if not r_cards:
        return create_embed(_("card_not_found")), True

    card = random.choice(r_cards)
    embed = resolve_search([card])
    return embed, False


def look_for_framework(query):
    """Given a query, returns a embed containing a timing of the game.

    Arguments:
        query -- A query

    Returns:
        A Discord.Embed with the timing of the query
    """
    embed = timings.find_formatted_timing(query)
    return embed, False


def look_for_preview_player_card(query: dict):
    """
    Given a query,
    returns a embed containing the information of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    for i in range(len(preview.get_preview_data()) // 25, -1, -1):
        if "card" + str(i) in query:
            r_cards = [
                c
                for c in preview.get_preview_data()
                if c["code"] == query["card" + str(i)]
            ]
            embed = resolve_search(r_cards)
            return embed, False

    return create_embed(_("card_not_found")), True


def look_for_whom(query: dict):
    """
    Given a query, returns an embed containing all the investigators who can take a card
    :param query:
    :return:
    """
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords)
    if not r_cards:
        return create_embed(_("card_not_found")), True

    embed = resolve_search_who(r_cards)
    return embed, False


def look_for_customizable_card(query: dict):
    """
    Given a query, returns an embed a the upgrade sheet of a customizable card
    :param query:
    :return:
    """

    r_cards = [c for c in cards.get_customizable_cards() if c["code"] == query["name"]]
    if not r_cards:
        return create_embed(_("card_not_found")), True

    embed = resolve_customizable(r_cards)
    return embed, False
