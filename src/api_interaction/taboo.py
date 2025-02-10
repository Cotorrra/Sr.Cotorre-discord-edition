import json

from config import LANG
from src.core.formatting import format_text
from src.core.translator import locale as _


class Taboo:
    """Class that handles the taboo data."""

    def __init__(self, current_taboo=""):
        if not current_taboo:
            with open(f"data/{LANG}/taboo.json", encoding="UTF-8") as f:
                self.taboo_data = json.load(f)
            current_taboo = self.taboo_data[0]["code"]
        self.current_taboo = current_taboo

    def get_taboo_info(self, taboo_ver="") -> list[dict[str, str]]:
        """
        Gets the taboo card information, according to the taboo version.
        :param taboo_ver: The taboo version (004, 003, etc.)
        :return:
        """
        return self.get_taboo(taboo_ver)["cards"]

    def get_taboo(self, taboo_ver="") -> dict[str, list[dict]]:
        """Gets the taboo card information, according to the taboo version.

        Keyword Arguments:
            taboo_ver: The Taboo Version 001-008  (default: "")

        Returns:
            dict: The taboo data.
        """
        current_taboo = taboo_ver if taboo_ver else self.current_taboo
        for info in self.taboo_data:
            if info["code"] == current_taboo:
                return info
        return {"cards": []}

    def is_in_taboo(self, card_id, taboo_ver=""):
        """
        Checks if a card is in the taboo list or not
        :param taboo_ver:
        :param card_id:
        :return:
        """
        tabooed_cards = self.get_taboo_info(taboo_ver)
        for card in tabooed_cards:
            if card["code"] == card_id:
                return True
        return False

    def get_tabooed_card(self, card_id, taboo_ver="") -> dict[str, str]:
        """
        Returns the card information from the current or given taboo information.
        :param taboo_ver:
        :param card_id:
        :return:
        """
        tabooed_cards = self.get_taboo_info(taboo_ver)
        for card in tabooed_cards:
            if card["code"] == card_id:
                return card
        return {}

    def calculate_xp(self, c: dict, qty: int, taboo_ver="") -> int:
        """Calculates the XP of a card, considering the quantity and the taboo version.

        Arguments:
            c -- The card
            qty -- The quantity of the card

        Keyword Arguments:
            taboo_ver -- The taboo version (default: {""})

        Returns:
            int -- The total XP of the card.
        """
        chain = 0
        taboo_exceptional = False
        if self.is_in_taboo(c["code"]):
            taboo_info = self.get_tabooed_card(c["code"], taboo_ver)
            if "xp" in taboo_info:
                chain = int(taboo_info["xp"])
            if "exceptional" in taboo_info:
                taboo_exceptional = taboo_info["exceptional"]

        if "xp" in c:
            if c["myriad"] or "Myriad." in c["real_text"]:
                return c["xp"] + chain
            if c["exceptional"] or taboo_exceptional:
                # Aunque debería haber 1 en el mazo...
                return (c["xp"] * 2 + chain) * qty

            return (c["xp"] + chain) * qty

        return chain * qty

    def format_xp(self, c, taboo_info=""):
        """Formats the XP of a card."""
        chain = ""
        text = ""
        if taboo_info:
            if self.is_in_taboo(c["code"], taboo_info):
                taboo_info = self.get_tabooed_card(c["code"], taboo_info)
                if "xp" in taboo_info:
                    xp = int(taboo_info["xp"])
                    sign = "+" if xp > 0 else ""
                    chain += f" {sign}{taboo_info['xp']}"
                if "exceptional" in taboo_info:
                    chain += " +E" * int(taboo_info["exceptional"])
        if "xp" in c:
            if "customization_text" in c:
                text = f" (C){chain}"
            elif c["xp"] == 0:
                text = f"{chain}"
            elif "exceptional" in c and c["exceptional"]:
                text = f" ({c['xp']}E){chain}"

            else:
                text = f" ({c['xp']}){chain}"
        else:
            text = ""
        return text

    def format_taboo_text(self, card_id):
        """Formats the taboo text of a card."""
        text = f"> **{_('taboo_title')}:** _({self.get_taboo_version()})_\n"
        if self.is_in_taboo(card_id):
            card = self.get_tabooed_card(card_id)
            if "xp" in card:
                xp = int(card["xp"])
                if xp >= 0:
                    text += f"> {_('taboo_chained')}: +{card['xp']} {_('xp')}\n"
                else:
                    text += f"> {_('taboo_unchained')}: {card['xp']} {_('xp')}\n"
            if "text" in card:
                text += f"> {format_text(card['text'])} \n"
            text += "\n"
            return text

        return ""

    def get_taboo_version(self):
        """Returns the current taboo version."""
        return self.get_taboo()["name"]


taboo = Taboo()
