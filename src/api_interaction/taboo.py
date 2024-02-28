import requests

from config import LANG, DATA_API
from src.core.formating import format_text
from src.core.translator import lang


class Taboo:
    def __init__(self):
        params = {"language": LANG,
                  "type": "taboo"}
        self.taboo_data = requests.get(f'{DATA_API}',
                                       params=params).json()

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
        for info in self.taboo_data:
            if info['active'] and not taboo_ver:
                return info
            if info['code'] == taboo_ver and taboo_ver:
                return info
            
        return {'cards': []}

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

    def calculate_xp(self, c, qty, taboo_ver="", deck_meta={}):
        upgrades_codes = []
        upgrades_xp = 0
        if c['code'] in deck_meta:
            card_meta = deck_meta[c['code']]
            for upgrade_id, upgrade_info in card_meta.items():
                if int(upgrade_info['xp']) > 0:
                    upgrades_codes.append(upgrade_id)
                    upgrades_xp += int(upgrade_info['xp'])

        chain = 0
        taboo_exceptional = False
        if self.is_in_taboo(c['code']):
            taboo_info = self.get_tabooed_card(c['code'], taboo_ver)
            if 'xp' in taboo_info:
                chain = taboo_info['xp']
            if 'exceptional' in taboo_info:
                taboo_exceptional = taboo_info['exceptional']
            if "xp_customizable" in taboo_info:
                for taboo_upgrade_id, taboo_upgrade_info in taboo_info["xp_customizable"].items():
                    if taboo_upgrade_id in upgrades_codes:
                        if 'xp' in taboo_upgrade_info:
                            upgrades_xp += int(taboo_upgrade_info['xp'])

        if "xp" in c:
            if c['myriad'] or 'Myriad.' in c['real_text']:
                return c['xp'] + chain + upgrades_xp 
            elif c['exceptional'] or taboo_exceptional:
                # Aunque debería haber 1 en el mazo...
                return (c['xp'] * 2 + chain) + upgrades_xp 
            else:
                return (c['xp'] + chain) * qty + upgrades_xp 
        else:
            return chain * qty + upgrades_xp 

    def format_xp(self, c, taboo_info="", deck_meta={}):
        chain = ""
        text = ""
        customizable_text = ""
        xp_customizable_info = {}
        if taboo_info:
            if self.is_in_taboo(c['code'], taboo_info):
                taboo_info = self.get_tabooed_card(c['code'], taboo_info)
                if 'xp' in taboo_info:
                    sign = "+" if taboo_info['xp'] > 0 else ""
                    chain += f" {sign}{taboo_info['xp']}"
                if 'exceptional' in taboo_info:
                    chain += " +E" * taboo_info['exceptional']
                if 'xp_customizable' in taboo_info:
                    for taboo_upgrade_id, taboo_upgrade_info in taboo_info["xp_customizable"].items():
                        xp_customizable_info[taboo_upgrade_id] = taboo_upgrade_info['xp']
                    # Old implementation
                    # for taboo_upgrade in taboo_info["xp_customizable"].split(","):
                    #    upgrade_loc, upgrade_chain = taboo_upgrade.split("|")
                    #    xp_customizable_info[upgrade_loc] = upgrade_chain
        
        # Thanks TSK
        upgrades_xp = 0
        upgrade_chain = 0
        if c['code'] in deck_meta:
            card_meta = deck_meta[c['code']]
            additional_info= []
            # card_upgrades = card_meta.split(",")
            info_text = ""
            for upgrade_id, upgrade_info in card_meta.items():
                    # upgrade_info = upgrade.split("|")
                    
                if int(upgrade_info['xp']) > 0:
                    upgrades_xp += int(upgrade_info['xp'])
                    if len(upgrade_info) > 1:
                        if c['code'] != '09080':
                            # Summoned Servitor has extra info, but is used for the slot choice
                            additional_info += upgrade_info['info'].split("^")
                    if upgrade_id in xp_customizable_info:
                        upgrade_chain += int(xp_customizable_info[upgrade_id])

                elif c['code'] in ['09042', '09060', '09079', '09101'] and upgrade_id == '0':
                    #  Friends of low places, Ravens Quill, Living Ink and Grizzled have initial info
                    additional_info += upgrade_info['info'].split("^")

            for text in additional_info:
                if c['code'] == '09079': # Living Ink has attributes
                        info_text += f"[{text}], "
                else:
                    info_text += f"<i>{text}</i>, "
            
            customizable_text = f"[{upgrades_xp}"
            if upgrade_chain:
                customizable_text += f"+{upgrade_chain}" if upgrade_chain > 0 else f"{upgrade_chain}"
            customizable_text += "pts"
            customizable_text += f", {format_text(info_text)[:-2]}]" if info_text else "]"
        
        if "xp" in c:
            if 'customization_text' in c:
                if upgrades_xp > 0:
                    text = f" ({(upgrades_xp + 1)//2}){chain} {customizable_text}"
                else:
                    text = f"{chain} {customizable_text}"
            elif c['xp'] == 0:
                text = f"{chain}"
            elif 'exceptional' in c and c['exceptional']:
                text = f" ({c['xp']}E){chain}"

            else:
                text = f" ({c['xp']}){chain}"
        else:
            text = ""

        return text

    def format_taboo_text(self, card_id):
        text = f"> **{lang.locale('taboo_title')}:** _({self.get_taboo_version()})_\n"
        if self.is_in_taboo(card_id):
            card = self.get_tabooed_card(card_id)
            if 'xp' in card:
                if card['xp'] >= 0:
                    text += f"> {lang.locale('taboo_chained')}: +{card['xp']} {lang.locale('xp')} \n"
                else:
                    text += f"> {lang.locale('taboo_unchained')}: {card['xp']} {lang.locale('xp')} \n"
            if 'text' in card:
                text += "> %s \n" % format_text(card['text'])
            text += "\n"
            return text
        else:
            return ""

    def get_taboo_version(self):
        return self.get_taboo()['name']


taboo = Taboo()
