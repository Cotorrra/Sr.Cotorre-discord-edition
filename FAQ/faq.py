import json

from core.formating import format_text


def load_faq():
    """
    Carga el archivo de taboo.
    :return:
    """
    with open('FAQ/data/faq.json') as errata:
        info = json.load(errata)

    info['cards'] = json.dumps(info['cards'])
    info['cards'] = json.loads(info['cards'])

    return info


def has_faq(card_id):
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


def get_faq(card_id):
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


def format_faq_text(card_id, back=False):
    text = "**Preguntas Frecuentes**: \n"
    if has_faq(card_id):
        card = get_faq(card_id)
        if back and ('text_back' in card):
            text += ">>> %s \n" % format_text(card['text_back'])
        elif 'text' in card:
            text += ">>> %s \n" % format_text(card['text'])
        return text
    else:
        return "Esta carta no tiene FAQ _(aún)_"


errata_info = load_faq()
