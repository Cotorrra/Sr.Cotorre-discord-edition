import random

from src.core.search import hits_in_string
from src.tarot.tarot import load_tarot


def search_for_tarot(query: str):
    tarot = load_tarot()
    if query:
        search = sorted(tarot['tarot'],
                        key=lambda con: - hits_in_string(query, con['name']))
    else:
        search = tarot['tarot'].copy()
        random.shuffle(search)
    if search:
        return search[0]
    else:
        return {}
