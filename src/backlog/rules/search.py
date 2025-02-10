from src.core.search import hits_in_string
from src.backlog.rules.rules import rules_info


def search_for_rules(query: str):
    """Searches for a rule in the rules.json"""
    rules = rules_info.get_rules()
    search = sorted(
        rules["rules"],
        key=lambda con: -hits_in_string(query, con["title"])
        - 3 * hits_in_string(query, con["keyword"]),
    )
    if search:
        return search[0]
    return {}
