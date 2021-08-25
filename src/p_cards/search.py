from src.core.utils import is_lvl


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


def format_query_pc(nombre, nivel, clase, extras, subtitulo, pack):
    subtitle = f" ~{subtitulo}~" if subtitulo else ""
    lvl_txt = str(nivel) if nivel != "" else ""
    extra = f" ({lvl_txt + clase + extras})" if nivel or clase or extras else ""
    package = f" [{pack}]" if pack else ""
    return nombre + subtitle + extra + package
