from src.core.utils import is_lvl


def use_pc_keywords(cards: list, query: dict):
    """
    Filtra cartas de jugador según los caracteres del string dado
    :param cards: Lista de cartas
    :param key_list: Argumentos dados
    :return:
    """
    filtered_cards = cards.copy()
    char = query['extras']
    if char.isdigit():
        filtered_cards = [c for c in filtered_cards if is_lvl(c, int(char))]
    if char == "e":
        filtered_cards = [c for c in filtered_cards if c['exceptional']]
    if char == "b":
        filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'seeker']
    if char == "g":
        filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'guardian']
    if char == "r":
        filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'rogue']
    if char == "s":
        filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'survivor']
    if char == "m":
        filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'mystic']
    if char == "n":
        filtered_cards = [c for c in filtered_cards if c['faction_code'] == 'neutral']
    if char == "mult":
        filtered_cards = [c for c in filtered_cards if ['faction2_code'] in c]
    if char == "u":
        filtered_cards = [c for c in filtered_cards if
                          (c['is_unique'] if 'is_unique' in c else False)]
    if char == "p":
        filtered_cards = [c for c in filtered_cards if c['permanent']]
    if char == "c":
        filtered_cards = [c for c in filtered_cards if "deck only." in c['real_text']]
    if char == "a":
        filtered_cards = [c for c in filtered_cards if c['code'][:2] == "90"]

    return filtered_cards
