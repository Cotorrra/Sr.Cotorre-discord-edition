import json

from core.formating import format_text


def load_concepts():
    """
    Carga el archivo de taboo.
    :return:
    """
    with open('concepts/data/concepts.json', encoding='utf-8') as faq:
        info = json.load(faq)

    info['cards'] = json.dumps(info['cards'])
    info['cards'] = json.loads(info['cards'])

    return info


def search_for_concept(query:str):
    return ""



def format_faq_text(card_id, back=False):
    return ""


faq_info = load_concepts()
