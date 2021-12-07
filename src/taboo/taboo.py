import requests

from config import LANG, DATA_API


class Taboo:
    def __init__(self, current_taboo):
        params = {"language": LANG,
                  "type": "taboo"}
        self.taboo_data = requests.get(f'{DATA_API}',
                                       params=params).json()
        self.current_taboo = current_taboo

    def reload_taboo(self):
        """
        Reloads the taboo information
        :return:
        """
        params = {"language": LANG,
                  "type": "taboo"}
        self.taboo_data = requests.get(f'{DATA_API}',
                                       params=params).json()

    def get_taboo_info(self, taboo_ver=""):
        """
        Gets the taboo information, according to the taboo version.
        :param taboo_ver: The taboo version (004, 003, etc.)
        :return:
        """
        current_taboo = taboo_ver if taboo_ver else self.current_taboo
        for info in self.taboo_data:
            if info['code'] == current_taboo:
                return info['cards']
        return []

    def is_in_taboo(self, card_id, taboo_ver=""):
        """
        Checks if a card is in the taboo list or not
        :param taboo_ver:
        :param card_id:
        :return:
        """
        tabooed_cards = self.get_taboo_info(taboo_ver)
        for card in tabooed_cards:
            if card['code'] == card_id:
                return True
        return False

    def get_tabooed_card(self, card_id, taboo_ver=""):
        """
        Devuelve la informacion de la carta dada en la informacion de tabú actual o dada.
        :param taboo_ver:
        :param card_id:
        :return:
        """
        tabooed_cards = self.get_taboo_info(taboo_ver)
        for card in tabooed_cards:
            if card['code'] == card_id:
                return card
        return {}

    def calculate_xp(self, c, qty, taboo_ver=""):
        chain = 0
        if self.is_in_taboo(c['code']):
            if 'xp' in self.get_tabooed_card(c['code'], taboo_ver):
                chain = self.get_tabooed_card(c['code'], taboo_ver)['xp']

        if "xp" in c:
            if c['myriad'] or 'Myriad.' in c['real_text']:
                return c['xp'] + chain
            elif c['exceptional']:
                # Aunque debería haber 1 en el mazo...
                return (c['xp'] + chain) * 2 * qty
            else:
                return (c['xp'] + chain) * qty
        else:
            return chain * qty


taboo_data = Taboo(current_taboo="004")
