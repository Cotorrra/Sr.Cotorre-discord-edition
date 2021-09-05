import json
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


errata_info = load_errata()
