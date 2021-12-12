import random

from src.core.search import hits_in_string
from src.tarot.tarot import tarot_data


def search_for_tarot(query: str):
    tarot = tarot_data.get_tarot_data()
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
