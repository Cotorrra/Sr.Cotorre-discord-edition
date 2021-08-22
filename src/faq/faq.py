import json

from src.core.formating import format_text
from src.core.utils import load_from_repo


def load_faq(card_id):
    """
    Carga el archivo de taboo.
    :return:
    """
    code = card_id[:2]
    file_src = f'data/faq/faq{code}.json'
    info = load_from_repo(file_src)

    info['cards'] = json.dumps(info['cards'])
    info['cards'] = json.loads(info['cards'])

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


def format_faq_text(card_id, back=False):
    faq_info = load_faq(card_id)
    text = "**Preguntas frecuentes**: \n"
    if has_faq(card_id, faq_info):
        card = get_faq(card_id, faq_info)
        if back and ('text_back' in card):
            text += ">>> %s \n" % format_text(card['text_back'])
        elif 'text' in card:
            text += ">>> %s \n" % format_text(card['text'])
        return text
    else:
        return "Esta carta no tiene faq _(aún)_"

