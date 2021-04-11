import requests

from decks.deck import check_upgrade_rules
from decks.formating import format_upgraded_deck


def find_deck(code: str):
    link = 'https://es.arkhamdb.com/api/public/deck/%s' % code
    req = requests.get(link)
    if req.url != link:
        link = 'https://es.arkhamdb.com/api/public/decklist/%s' % code
        req = requests.get(link)
        if req.url != link:
            return {}
    return req.json()


def find_former_deck(code: str):
    curr_deck = find_deck(code)
    if curr_deck:
        former_code = str(curr_deck['previous_deck'])
        former_deck = find_deck(former_code)
        if former_deck:
            return former_deck
        else:
            return False
    return False


def search_for_upgrades(code, cards):
    deck1 = find_deck(code)
    deck2 = find_former_deck(code)
    if not deck1:
        response = "No encontré el mazo."
        embed = False
    elif not deck2:
        response = "El Mazo dado no contiene una mejora."
        embed = False
    else:
        info = check_upgrade_rules(deck2, deck1, cards)
        response = "¡Encontré una Mejora!"
        embed = format_upgraded_deck(deck1, info)

    return response, embed
