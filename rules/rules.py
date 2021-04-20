import json

from core.formating import format_text
from core.search import hits_in_string


def load_rules():
    """
    Carga el archivo de taboo.
    :return:
    """
    with open('rules/data/rules.json', encoding='utf-8') as faq:
        info = json.load(faq)

    info['rules'] = json.dumps(info['rules'])
    info['rules'] = json.loads(info['rules'])

    return info


def search_for_rules(query: str):
    rules = load_rules()
    search = sorted(rules['rules'],
                    key=lambda con: - hits_in_string(query, con['title']) - 3 * hits_in_string(query, con['keyword'],
                                                                                               False))
    if search:
        return search[0]
    else:
        return {}
