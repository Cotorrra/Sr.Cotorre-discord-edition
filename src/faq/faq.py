import requests

from config import LANG, DATA_API


def load_faq():
    """
    Carga el archivo de taboo.
    :return:
    """
    params = {"language": LANG,
              "type": "faq"}
    info = requests.get(f'{DATA_API}',
                        params=params).json()

    return info


def has_faq(card_id, faq_info):
    """
    Devuelve True si la carta posee faq
    :param faq_info:
    :param card_id:
    :return:
    """
    for card in faq_info['cards']:
        if card['code'] == card_id:
            return True
    return False


def get_faq(card_id, faq_info):
    """
    Devuelve la informacion de la carta dada en la informacion de faq.
    :param faq_info: Información del faq
    :param card_id: Id de la carta
    :return:
    """
    for card in faq_info['cards']:
        if card['code'] == card_id:
            return card
    return {}


