"""
    Encounter Card Search/Filter
"""


def use_ec_keywords(cards: list, query: dict):
    """
    Filter encounter cards according to the key_list
    :param cards: Encounter card list
    :param query: Filter parameters
    :return:
    """
    # TODO: Rework this info reading all the info from key_list
    filtered_c = cards.copy()
    if query['type']:
        char = query['type'].lower()
        if char == "e":
            filtered_c = [c for c in filtered_c if c['type_code'] == "enemy"]
        if char == "a":
            filtered_c = [c for c in filtered_c if c['type_code'] == "act"]
        if char == "p":
            filtered_c = [c for c in filtered_c if c['type_code'] == "agenda"]
        if char == "t":
            filtered_c = [c for c in filtered_c if c['type_code'] == "treachery"]
        if char == "s":
            filtered_c = [c for c in filtered_c if c['type_code'] == "scenario"]
        if char == "l":
            filtered_c = [c for c in filtered_c if c['type_code'] == "location"]
        if char == "j":
            filtered_c = [c for c in filtered_c if c['type_code'] in ['asset', 'event', 'skill']]

    return filtered_c
