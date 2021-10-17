import requests
import shutil

from config import arkhamdb
from src.core.formating import create_embed
from src.core.translator import locale
from src.faq.formating import format_faq
from src.backs.search import resolve_back_search
from src.core.resolve import resolve_search
from src.core.search import card_search
from src.decks.deck import extract_deck_info, check_upgrade_rules
from src.decks.formating import format_deck, format_upgraded_deck
from src.decks.search import find_deck, find_former_deck
from src.e_cards.search import use_ec_keywords
from src.p_cards.search import use_pc_keywords
from src.rules.formating import format_rule
from src.rules.search import search_for_rules
from src.tarot.formating import format_tarot
from src.tarot.search import search_for_tarot


# This class contains the cards from ArkhamDB
class CardsDB:
    def __init__(self):
        self.ah_all_cards = requests.get(f'{arkhamdb}/api/public/cards?encounter=1').json()
        self.ah_player = requests.get(f'{arkhamdb}/api/public/cards?encounter=0').json()
        self.ah_encounter = [c for c in self.ah_all_cards if "spoiler" in c]

    def get_all_cards(self):
        return self.ah_all_cards

    def get_p_cards(self):
        return self.ah_player

    def get_e_cards(self):
        return self.ah_encounter

    def refresh(self):
        self.ah_all_cards = requests.get(f'{arkhamdb}/api/public/cards?encounter=1').json()
        self.ah_player = requests.get(f'{arkhamdb}/api/public/cards?encounter=0').json()
        self.ah_encounter = [c for c in self.ah_all_cards if "spoiler" in c]
        shutil.rmtree('/data/', ignore_errors=True)
        return True


cards = CardsDB()


def refresh_cards():
    """
    Refreshes the cards from ArkhamDB
    :return:
    """
    return cards.refresh()


def look_for_player_card(query: str):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :param cards: The cards to search from
    :param keyword_fun: A function that filters cards given the keywords in (TYPE)
    :return: a Discord.Embed
    """
    r_cards = card_search(query, cards.get_p_cards(), use_pc_keywords)
    embed = resolve_search(r_cards)
    if embed:
        return embed
    else:
        return create_embed(locale('card_not_found'), "", {})


def look_for_mythos_card(query: str):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a mythos card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    r_cards = card_search(query, cards.get_e_cards(), use_ec_keywords)
    embed = resolve_search(r_cards)
    if not embed:
        embed = create_embed(locale('card_not_found'), "", {})

    return embed


def look_for_card_back(query: str):
    """
    Given a query, a list of cards and a keyword function
    returns a embed containing the information of a back of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return: a Discord.Embed
    """
    f_cards = [c for c in cards.get_all_cards() if c["double_sided"]]
    r_cards = card_search(query, f_cards, use_ec_keywords)
    embed = resolve_back_search(r_cards)
    if not embed:
        embed = create_embed(locale('card_not_found'), "", {})

    return embed


def look_for_deck(code, deck_type):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed that contains the information of that deck.
    :param deck_type:
    :param code: ArkhamDB ID
    :return:
    """
    deck = find_deck(code, deck_type)
    if not deck:
        embed = create_embed(locale('deck_not_found'), "", {})
    else:
        deck_info = extract_deck_info(deck, cards.get_all_cards())
        embed = format_deck(deck, deck_info)
    return embed


def look_for_upgrades(code, deck_mode):
    """
    Given a ArkhamDB deckcode, returns a Discord.Embed that contains the upgrade information of that deck if any.
    :param deck_mode:
    :param code: ArkhamDB ID
    :return:
    """
    deck1 = find_deck(code, deck_mode)
    deck2 = find_former_deck(code, deck_mode)
    if not deck1:
        embed = create_embed(locale('deck_not_found'))
    elif not deck2:
        embed = create_embed(locale('upgrade_not_found'))
    else:
        info = check_upgrade_rules(deck2, deck1, cards.get_p_cards())
        embed = format_upgraded_deck(deck1, info)

    return embed


def look_for_faq(query):
    """
    Given a query, returns a embed containing the faq of a card.
    :param query: A query string, it can contain an (TYPE) or a ~Subtext~
    :return:
    """
    r_cards = card_search(query, cards.get_all_cards(), use_ec_keywords)
    if r_cards:
        embed = format_faq(r_cards[0])
    else:
        embed = create_embed(locale('card_not_found'), "", {})
    return embed


def look_for_rule(query):
    """
    Given a query, returns a embed containing a rule of the game
    :param query:  A query string.
    :return:
    """
    search = search_for_rules(query)
    if search:
        embed = format_rule(search)
    else:
        embed = create_embed(locale('card_not_found'), "", {})
    return embed


def look_for_tarot(query):
    """
    Given a query, returns a embed containing a tarot card of the game.
    If the query is empty, returns a random tarot card.
    :param query:  A query string.
    :return:
    """
    search = search_for_tarot(query)
    if search:
        embed = format_tarot(search)
    else:
        embed = create_embed(locale('card_not_found'), "", {})

    return embed


