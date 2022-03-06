import requests

from config import DATA_API, LANG
from src.core.formating import format_text, create_embed


class Timings:
    def __init__(self):
        params = {"language": LANG,
                  "type": "timings"}
        self.timings = requests.get(f'{DATA_API}',
                                    params=params).json()

    def reload_timings(self):
        """
        Carga el archivo de taboo.
        :return:
        """
        params = {"language": LANG,
                  "type": "timings"}
        self.timings = requests.get(f'{DATA_API}',
                                    params=params).json()

    def get_timings_data(self):
        return self.timings

    def find_formated_timing(self, query):
        timing = self.timings['framework'][query]
        name, text = next(iter(timing.items()))
        title = f"**{name}**"
        description = ">>> "
        for line in text:
            description += f"{format_text(line)}\n"
        embed = create_embed(title=title, description=description)
        return embed


timings = Timings()
