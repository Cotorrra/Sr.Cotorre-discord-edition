import json
from src.core.formating import format_text
from src.core.utils import load_from_repo


def load_errata():
    """
    Carga el archivo de taboo.
    :return:
    """
    file_src = 'data/errata/errata.json'
    info = load_from_repo(file_src)

    info['cards'] = json.dumps(info['cards'])
    info['cards'] = json.loads(info['cards'])

    return info


def has_errata(card_id):
    """
    Devuelve True si la carta posee una errata
    :param card_id:
    :param version:
    :return:
    """
    for card in errata_info['cards']:
        if card['code'] == card_id:
            return True
    return False


def get_errata_card(card_id):
    """
    Devuelve la informacion de la carta dada en la informacion de erratas.
    :param card_id:
    :param version:
    :return:
    """
    for card in errata_info['cards']:
        if card['code'] == card_id:
            return card
    return {}


def format_errata_text(card_id, back=False):
    text = "> **Errata**:\n"
    if has_errata(card_id):
        card = get_errata_card(card_id)
        if back and ('text_back' in card):
            text += "> %s \n" % format_text(card['text_back'])
        elif 'text' in card:
            text += "> %s \n" % format_text(card['text'])
        return text
    else:
        return ""


errata_info = load_errata()
