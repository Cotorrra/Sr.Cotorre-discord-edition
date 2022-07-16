import requests

from config import DATA_API, LANG


class Preview:
    def __init__(self):
        params = {"language": LANG,
                  "type": "preview"}
        self.preview = requests.get(f'{DATA_API}',
                                    params=params).json()

    def reload_preview(self):
        """
        Carga el archivo de taboo.
        :return:
        """
        params = {"language": LANG,
                  "type": "preview"}
        self.preview = requests.get(f'{DATA_API}',
                                    params=params).json()

    def get_preview_data(self):
        return self.preview['cards']


preview = Preview()
