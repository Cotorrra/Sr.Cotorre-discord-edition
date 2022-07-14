import requests

from config import ARKHAM_DB


class CardsDB:
    """
    This class contains the cards from ArkhamDB, with its Errata, Taboo and Tarot data.
    """
    def __init__(self):
        self.ah_all_cards = requests.get(f'{ARKHAM_DB}/api/public/cards?encounter=1').json()
        self.ah_player = requests.get(f'{ARKHAM_DB}/api/public/cards?encounter=0').json()
        self.ah_player = [c for c in self.ah_player if "duplicate_of_code" not in c and not c['faction_code'] == 'mythos']
        self.ah_encounter = [c for c in self.ah_all_cards if "spoiler" in c]

    def get_all_cards(self):
        return self.ah_all_cards

    def get_p_cards(self):
        return self.ah_player

    def get_e_cards(self):
        return self.ah_encounter

    def refresh(self):
        self.ah_all_cards = requests.get(f'{ARKHAM_DB}/api/public/cards?encounter=1').json()
        self.ah_player = requests.get(f'{ARKHAM_DB}/api/public/cards?encounter=0').json()
        self.ah_encounter = [c for c in self.ah_all_cards if "spoiler" in c]
        self.ah_player = [c for c in self.ah_player if "duplicate_of_code" not in c]


cards = CardsDB()
