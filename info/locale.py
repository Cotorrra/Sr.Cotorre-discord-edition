import requests

from config import LANG, DATA_API


class Locale:
    def __init__(self):
        self.lang = LANG
        self.current_lang = self.reload_language()

    def reload_language(self):
        """
        Load the language file from the DATA_API
        :return:
        """
        with open(f"{self.lang}/lang.json") as json_lang:
            info = ...

        return info

    def locale(self, tag):
        return self.current_lang['lang'][tag]


lang = Locale()
