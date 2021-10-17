import json

import requests

from config import arkhamdb


def find_deck(code: str, deck_mode):
    try:
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
    except json.decoder.JSONDecodeError:
        return {}


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


