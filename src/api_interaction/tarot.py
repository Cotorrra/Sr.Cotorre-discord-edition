import requests
import random

from config import LANG, DATA_API

from src.core.formating import format_text, create_embed
from src.core.search import hits_in_string
from src.core.translator import lang


class Tarot:
    def __init__(self):
        params = {"language": LANG,
                  "type": "tarot"}
        self.tarot_info = requests.get(f'{DATA_API}',
                                       params=params).json()

    def reload_tarot(self):
        """
        Carga el archivo de taboo.
        :return:
        """
        params = {"language": LANG,
                  "type": "tarot"}
        self.tarot_info = requests.get(f'{DATA_API}',
                                       params=params).json()

    def get_tarot_data(self):
        return self.tarot_info

    def search_for_tarot(self, query: str):
        if query:
            search = sorted(self.tarot_info['tarot'],
                            key=lambda con: - hits_in_string(query, con['name']))
        else:
            search = self.tarot_info['tarot'].copy()
            random.shuffle(search)
        if search:
            return search[0]
        else:
            return {}


def format_tarot(tarot_card):
    title = f"**{tarot_card['name']}**"
    up_text = format_text(tarot_card['up'])
    down_text = format_text(tarot_card['down'])
    orientation = random.choice([lang.locale('tarot_up_name'), lang.locale('tarot_down_name')])
    description = f"**{lang.locale('tarot_title')}** _({orientation})_" \
                  f"\n\n***{lang.locale('tarot_up_name')}***" \
                  f"\n> {up_text}" \
                  f"\n\n***{lang.locale('tarot_down_name')}***" \
                  f"\n> {down_text}" \

    footnote = f"🖌{tarot_card['illustrator']}" \
               f"\n{tarot_card['set']} #{tarot_card['number']}."
    embed = create_embed(title=title, description=description, footnote=footnote)

    return embed


tarot = Tarot()
