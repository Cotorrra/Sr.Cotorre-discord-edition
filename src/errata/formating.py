from src.core.formating import format_card_text
from src.core.translator import lang
from src.errata.errata import errata_data


def format_errata_text(card_id, back=False):
    text = ""
    if errata_data.has_errata(card_id):
        card = errata_data.get_errata_card(card_id)
        if back and ('text_back' in card):
            text += f"> **{lang.locale('errata_title')}**:\n> %s \n\n" % format_card_text(card, 'text_back')
        elif 'text' in card:
            text += f"> **{lang.locale('errata_title')}**:\n> %s \n\n" % format_card_text(card, 'text')
        return text
    else:
        return ""
