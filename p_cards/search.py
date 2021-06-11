from core.utils import is_lvl


def use_pc_keywords(cards: list, key_list: str):
    """
    Filtra cartas de jugador según los caracteres del string dado
    :param cards: Lista de cartas
    :param key_list: Argumentos dados
    :return:
    """
    filtered_cards = cards
    for char in key_list.lower():
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
        if char == "u":
            filtered_cards = [c for c in filtered_cards if c['unique']]
        if char == "p":
            filtered_cards = [c for c in filtered_cards if c['permanent']]
        if char == "c":
            filtered_cards = [c for c in filtered_cards if "deck only." in c['real_text']]
        if char == "a":
            filtered_cards = [c for c in filtered_cards if "Advanced." in c['real_text']]

    return filtered_cards


def format_query_pc(kwargs):
    name = kwargs.get('nombre')
    subtitle = f" ~{kwargs.get('subtitulo')}~" if kwargs.get('subtitulo') else ""
    lvl = str(kwargs.get('nivel')) if "nivel" in kwargs else ""
    clase = kwargs.get('clase') if "clase" in kwargs else ""
    ex = kwargs.get('extras') if "extras" in kwargs else ""
    extra = f" ({lvl + clase + ex})" if lvl or clase or ex else ""
    pack = f" [{kwargs.get('pack')}]" if "pack" in kwargs else ""
    return name + subtitle + extra + pack
