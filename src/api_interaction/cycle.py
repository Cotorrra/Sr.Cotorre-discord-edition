import requests

from config import DATA_API, LANG


class Cycle:
    def __init__(self):
        params = {"language": LANG,
                  "type": "cycle"}
        self.cycle = requests.get(f'{DATA_API}',
                                  params=params).json()

    def reload_cycles(self):
        """
        Carga el archivo de taboo.
        :return:
        """
        params = {"language": LANG,
                  "type": "cycle"}
        self.cycle = requests.get(f'{DATA_API}',
                                  params=params).json()

    def get_cycle_data(self):
        return self.cycle['cycles']


cycle = Cycle()
