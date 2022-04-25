"""
    Encounter Card Search/Filter
"""
from src.core.utils import is_lvl


def use_ec_keywords(cards: list, key_list: str):
    """
    Filter encounter cards according to the key_list
    :param cards: Encounter card list
    :param key_list: Filter parameters
    :return:
    """
    filtered_cards = cards.copy()
    for char in key_list.lower():
        if char.isdigit():
            filtered_cards = [c for c in filtered_cards if is_lvl(c, int(char))]
        if char == "e":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "enemy"]
        if char == "a":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "act"]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "agenda"]
        if char == "t":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "treachery"]
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "scenario"]
        if char == "l":
            filtered_cards = [c for c in filtered_cards if c['type_code'] == "location"]
        if char == "j":
            filtered_cards = [c for c in filtered_cards if c['type_code'] in ['asset', 'event', 'skill']]
        if char == "m":
            filtered_cards = [c for c in filtered_cards if c['faction_code'] == "mythos"]

    return filtered_cards


