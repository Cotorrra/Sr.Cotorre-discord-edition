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
    filtered_cards = cards.copy()

    if "card_type" in query and query["card_type"]:
        char = query["card_type"].lower()
        if char == "e":
            filtered_cards = [c for c in filtered_cards if c["type_code"] == "enemy"]
        if char == "a":
            filtered_cards = [c for c in filtered_cards if c["type_code"] == "act"]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c["type_code"] == "agenda"]
        if char == "t":
            filtered_cards = [
                c for c in filtered_cards if c["type_code"] == "treachery"
            ]
        if char == "s":
            filtered_cards = [c for c in filtered_cards if c["type_code"] == "scenario"]
        if char == "l":
            filtered_cards = [c for c in filtered_cards if c["type_code"] == "location"]
        if char == "j":
            filtered_cards = [
                c
                for c in filtered_cards
                if c["type_code"] in ["asset", "event", "skill"]
            ]

    if "traits" in query and query["traits"]:
        traits = query["traits"].split(",")
        traits = [t.strip() for t in traits]
        filtered_cards = [c for c in filtered_cards if "traits" in c]

        for trait in traits:
            # This is a workaround to avoid the last dot in the traits
            filtered_cards = [
                c for c in filtered_cards if trait in c["traits"][:-1].split(". ")
            ]

    return filtered_cards
