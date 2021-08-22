import json

from src.core.formating import format_text
from src.core.search import hits_in_string
from src.core.utils import load_from_repo


def load_rules():
    """
    Carga el archivo de taboo.
    :return:
    """
    file_src = 'data/rules/rules.json'

    info = load_from_repo(file_src)

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
