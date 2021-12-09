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
        Gets the taboo card information, according to the taboo version.
        :param taboo_ver: The taboo version (004, 003, etc.)
        :return:
        """
        return self.get_taboo(taboo_ver)['cards']

    def get_taboo_ver(self, taboo_ver=""):
        """
        Gets the taboo card information, according to the taboo version.
        :param taboo_ver: The taboo version (004, 003, etc.)
        :return:
        """
        return self.get_taboo(taboo_ver)['date_start']

    def get_taboo(self, taboo_ver=""):
        current_taboo = taboo_ver if taboo_ver else self.current_taboo
        for info in self.taboo_data:
            if info['code'] == current_taboo:
                return info
        return {}

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
        taboo_exceptional = False
        if self.is_in_taboo(c['code']):
            taboo_info = self.get_tabooed_card(c['code'], taboo_ver)
            if 'xp' in taboo_info:
                chain = taboo_info['xp']
            if 'exceptional' in taboo_info:
                taboo_exceptional = taboo_info['exceptional'] == 1

        if "xp" in c:
            if c['myriad'] or 'Myriad.' in c['real_text']:
                return c['xp'] + chain
            elif c['exceptional'] or taboo_exceptional:
                # Aunque debería haber 1 en el mazo...
                return (c['xp'] * 2 + chain) * qty
            else:
                return (c['xp'] + chain) * qty
        else:
            return chain * qty


taboo_data = Taboo(current_taboo="004")
