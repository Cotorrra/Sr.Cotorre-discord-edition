import requests

from config import LANG, DATA_API


class Errata:

    def __init__(self):
        params = {"language": LANG,
                  "type": "errata"}
        self.errata_data = requests.get(f'{DATA_API}',
                                        params=params).json()

    def reload_errata(self):
        """
        Gets the errata information from the DATA_API link
        :return: the errata info
        """
        params = {"language": LANG,
                  "type": "errata"}
        self.errata_data = requests.get(f'{DATA_API}',
                                        params=params).json()

    def has_errata(self, card_id):
        """
        Returns True if the card has an errata.
        :param card_id: card id
        :return:
        """
        for card in self.errata_data['cards']:
            if card['code'] == card_id:
                return True
        return False

    def get_errata_card(self, card_id):
        """
        Return the errata info of a given card.
        :param card_id: the card's ArkhamDB ID
        :return: The errata information
        """
        for card in self.errata_data['cards']:
            if card['code'] == card_id:
                return card
        return {}


errata_data = Errata()
