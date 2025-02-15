import json
import logging
import requests

from config import ARKHAM_DB


def find_deck(code: str, deck_mode) -> dict:
    """Searchs a deck by code in the ArkhamDB API."""
    try:
        if deck_mode:
            link = f"{ARKHAM_DB}/api/public/{deck_mode}/{code}"
            req = requests.get(link, timeout=3)
            if not req.text:
                return {}
        else:
            link = f"{ARKHAM_DB}/api/public/decklist/{code}"
            req = requests.get(link, timeout=3)
            if not req.text:
                link = f"{ARKHAM_DB}/api/public/deck/{code}"
                req = requests.get(link, timeout=3)
                if not req.text:
                    return {}
        logging.info(f"Gotten Request: {req.json()}")
        return req.json()
    except json.decoder.JSONDecodeError:
        logging.error("JSONDecodeError")
        return {}


def find_former_deck(code: str, deck_mode):
    """Looks for a deck by its code, and returns its former deck in the upgrade list."""
    curr_deck = find_deck(code, deck_mode)
    if curr_deck:
        former_code = str(curr_deck["previous_deck"])
        former_deck = find_deck(former_code, deck_mode)
        if former_deck:
            return former_deck
        else:
            return False
    return False
