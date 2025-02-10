import json

from config import LANG


class FAQ:
    """Class that handles the FAQ data from the data/faq.json file."""

    def __init__(self):
        with open(f"data/{LANG}/faq.json", encoding="UTF-8") as f:
            self.faq_info = json.load(f)

    def has_faq(self, card_id):
        """
        Devuelve True si la carta posee faq
        :param card_id:
        :return:
        """
        for card in self.faq_info["cards"]:
            if card["code"] == card_id:
                return True
        return False

    def get_faq(self, card_id):
        """
        Devuelve la informacion de la carta dada en la informacion de faq.
        :param faq_info: Información del faq
        :param card_id: Id de la carta
        :return:
        """
        for card in self.faq_info["cards"]:
            if card["code"] == card_id:
                return card
        return {}


faq_info = FAQ()
