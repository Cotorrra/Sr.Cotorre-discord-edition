from src.core.formating import format_text
from src.taboo.taboo import current_taboo, is_in_taboo, get_tabooed_card


def format_taboo_text(card_id, version=current_taboo):
    text = "> **Tabú más reciente:** \n"
    if is_in_taboo(card_id, version):
        card = get_tabooed_card(card_id, version)
        if 'xp' in card:
            if card['xp'] >= 0:
                text += "> Encadenada: +%d de experiencia \n" % card['xp']
            else:
                text += "> Desencadenada: %d de experiencia \n" % card['xp']
        if 'text' in card:
            text += "> %s \n" % format_text(card['text'])
        text += "\n"
        return text
    else:
        return ""