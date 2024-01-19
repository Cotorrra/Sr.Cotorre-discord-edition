import requests

from config import ARKHAM_DB
from src.core.translator import lang
from src.core.utils import get_code


class CardsDB:
    """
    This class contains the cards from ArkhamDB, with its Errata, Taboo and Tarot data.
    """

    def __init__(self):
        self.ah_all_cards = requests.get(f'{ARKHAM_DB}/api/public/cards?encounter=1').json()
        self.ah_player = requests.get(f'{ARKHAM_DB}/api/public/cards?encounter=0').json()

        self.ah_player = [c for c in self.ah_player if
                          "duplicate_of_code" not in c and not c['faction_code'] == 'mythos']
        self.ah_encounter = [c for c in self.ah_all_cards if "spoiler" in c]
        self.ah_investigators = [c for c in self.ah_player if
                                 c['type_code'] == 'investigator' and
                                 'duplicate_of_code' not in c and  # NO Duplicates
                                 'deck_requirements' in c and  # No Bonded/Hank
                                 (1000 < get_code(c) < 70000 or # No Parallels/Books
                                  c['code'] == '98019')]  # Hello Gloria
        parallel_inv = [c for c in self.ah_player if
                        c['type_code'] == 'investigator' and
                        'duplicate_of_code' not in c and  # NO Duplicates
                        (90000 < get_code(c) < 98000)]
        for inv in parallel_inv:
            inv['name'] = f"{inv['name']} ({lang.locale('parallel')})"
        self.ah_investigators += parallel_inv
        self.ah_customizable = [c for c in self.ah_player if 'customization_text' in c]

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
        self.ah_customizable = [c for c in self.ah_player if 'customization_text' in c]

    def get_investigators(self):
        return self.ah_investigators

    def get_customizable_cards(self):
        return self.ah_customizable

cards = CardsDB()
