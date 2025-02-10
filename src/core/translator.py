import json

from config import LANG


class Locale:
    """Class that handles the locale data."""

    def __init__(self):
        self.lang = LANG
        with open(f"data/{self.lang}/lang.json", encoding="UTF-8") as f:
            self.current_lang = json.load(f)

    def locale(self, tag):
        """Translates a tag into the current language."""
        if tag in self.current_lang["lang"]:
            return self.current_lang["lang"][tag]
        return f"{tag} ({lang})"


lang = Locale()
locale = lang.locale
