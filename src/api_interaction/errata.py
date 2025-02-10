import json

from config import LANG
from src.core.formatting import format_card_text
from src.core.translator import locale as _


class Errata:
    """Class that handles the errata data from the data/errata.json file."""

    def __init__(self):
        with open(f"data/{LANG}/errata.json", encoding="UTF-8") as f:
            self.errata_data = json.load(f)

    def has_errata(self, card_id):
        """
        Returns True if the card has an errata.
        :param card_id: card id
        :return:
        """
        for card in self.errata_data["cards"]:
            if card["code"] == card_id:
                return True
        return False

    def get_errata_card(self, card_id):
        """
        Return the errata info of a given card.
        :param card_id: the card's ArkhamDB ID
        :return: The errata information
        """
        for card in self.errata_data["cards"]:
            if card["code"] == card_id:
                return card
        return {}

    def format_errata_text(self, card_id, back=False):
        """Formats the errata text into a markdown string."""
        text = ""
        if self.has_errata(card_id):
            card = self.get_errata_card(card_id)
            if back and ("text_back" in card):
                text += f"> **{_('errata_title')}**:\n> %s \n\n" % format_card_text(
                    card, "text_back"
                )
            elif "text" in card:
                text += f"> **{_('errata_title')}**:\n> %s \n\n" % format_card_text(
                    card, "text"
                )
            return text

        return ""


errata = Errata()
