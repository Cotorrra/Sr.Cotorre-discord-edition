from src.core.formating import format_text
from src.core.translator import lang
from src.taboo.taboo import taboo_data


def format_taboo_text(card_id):
    text = f"> **{lang.locale('taboo_title')}:** \n"
    if taboo_data.is_in_taboo(card_id):
        card = taboo_data.get_tabooed_card(card_id)
        if 'xp' in card:
            if card['xp'] >= 0:
                text += f"> {lang.locale('taboo_chained')}: +{card['xp']} {lang.locale('xp')} \n"
            else:
                text += f"> {lang.locale('taboo_unchained')}: {card['xp']} {lang.locale('xp')} \n"
        if 'text' in card:
            text += "> %s \n" % format_text(card['text'])
        text += "\n"
        return text
    else:
        return ""
