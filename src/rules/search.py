from src.core.search import hits_in_string
from src.rules.rules import load_rules


def search_for_rules(query: str):
    rules = load_rules()
    search = sorted(rules['rules'],
                    key=lambda con: - hits_in_string(query, con['title']) - 3 * hits_in_string(query, con['keyword'],
                                                                                               False))
    if search:
        return search[0]
    else:
        return {}

