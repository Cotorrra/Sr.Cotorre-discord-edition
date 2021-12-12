import requests

from config import LANG, DATA_API


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


tarot_data = Tarot()
