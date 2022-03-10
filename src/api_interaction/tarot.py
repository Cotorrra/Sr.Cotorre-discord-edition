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


def format_tarot(tarot):
    title = f"**{tarot['name']}**"
    up_text = format_text(tarot['up'])
    down_text = format_text(tarot['down'])
    description = f"**{lang.locale('tarot_title')}**" \
                      f"\n\n***{lang.locale('tarot_up_name')}***" \
                      f"\n> _{up_text}_" \
                      f"\n\n***{lang.locale('tarot_down_name')}***" \
                      f"\n> _{down_text}_" \
                      f"\n"
    footnote = f"🖌{tarot['illustrator']}" \
                   f"\n{tarot['set']} #{tarot['number']}."
    embed = create_embed(title=title, description=description, footnote=footnote)

    return embed


tarot = Tarot()
