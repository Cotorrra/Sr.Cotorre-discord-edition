import requests

from config import arkhamdb
from src.core.translator import locale
from src.decks.deck import check_upgrade_rules
from src.decks.formating import format_upgraded_deck


def find_deck(code: str, deck_mode):
    if deck_mode:
        link = f"{arkhamdb}/api/public/{deck_mode}/{code}"
        req = requests.get(link)
        if not req.text:
            return {}
    else:
        link = f"{arkhamdb}/api/public/decklist/{code}"
        req = requests.get(link)
        if not req.text:
            link = f"{arkhamdb}/api/public/deck/{code}"
            req = requests.get(link)
            if not req.text:
                return {}
    return req.json()


def find_former_deck(code: str, deck_mode):
    curr_deck = find_deck(code, deck_mode)
    if curr_deck:
        former_code = str(curr_deck['previous_deck'])
        former_deck = find_deck(former_code, deck_mode)
        if former_deck:
            return former_deck
        else:
            return False
    return False


def search_for_upgrades(code, cards, deck_mode):
    deck1 = find_deck(code, deck_mode)
    deck2 = find_former_deck(code, deck_mode)
    if not deck1:
        response = locale('deck_not_found')
        embed = False
    elif not deck2:
        response = locale('upgrade_not_found')
        embed = False
    else:
        info = check_upgrade_rules(deck2, deck1, cards)
        response = ""
        embed = format_upgraded_deck(deck1, info)

    return response, embed

