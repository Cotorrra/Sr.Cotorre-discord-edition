from src.core.formating import format_text
from src.core.translator import locale
from src.taboo.taboo import current_taboo, is_in_taboo, get_tabooed_card


def format_taboo_text(card_id, version=current_taboo):
    text = f"> **{locale('taboo_title')}:** \n"
    if is_in_taboo(card_id, version):
        card = get_tabooed_card(card_id, version)
        if 'xp' in card:
            if card['xp'] >= 0:
                text += f"> {locale('taboo_chained')}: +{card['xp']} {locale('xp')} \n"
            else:
                text += f"> {locale('taboo_unchained')}: {card['xp']} {locale('xp')} \n"
        if 'text' in card:
            text += "> %s \n" % format_text(card['text'])
        text += "\n"
        return text
    else:
        return ""
