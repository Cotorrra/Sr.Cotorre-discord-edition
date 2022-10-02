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
        params = {"language": self.lang,
                  "type": "lang"}
        info = requests.get(f'{DATA_API}', params=params).json()

        return info

    def locale(self, tag):
        if tag in self.current_lang['lang']:
            return self.current_lang['lang'][tag]
        else:
            return f"{tag} ({lang})"


lang = Locale()
