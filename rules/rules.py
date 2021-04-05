import json

from core.formating import format_text


def load_concepts():
    """
    Carga el archivo de taboo.
    :return:
    """
    with open('rules/data/rules.json', encoding='utf-8') as faq:
        info = json.load(faq)

    info['rules'] = json.dumps(info['rules'])
    info['rules'] = json.loads(info['rules'])

    return info


def search_for_concept(query: str):
    search = sorted(concepts['rules'],
                    key=lambda con: -hits_in_string(query, con['title']) - 3 * hits_in_string(query, con['keyword'], False))
    if search:
        return search[0]
    else:
        return {}


faq_info = load_concepts()
