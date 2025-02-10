import json
import random

from config import LANG

from src.core.formatting import format_text, create_embed
from src.core.search import hits_in_string
from src.core.translator import locale as _


class Tarot:
    """Class that handles the tarot data."""

    def __init__(self):
        with open(f"data/{LANG}/tarot.json", encoding="UTF-8") as f:
            self.tarot_info = json.load(f)

    def get_tarot_data(self):
        """Returns the tarot data from the JSON file.

        Returns:
            dict: The tarot data.
        """
        return self.tarot_info

    def search_for_tarot(self, query: str):
        """Searches for a tarot card."""
        if query:
            search = sorted(
                self.tarot_info["tarot"],
                key=lambda con: -hits_in_string(query, con["name"]),
            )
        else:
            search = self.tarot_info["tarot"].copy()
            random.shuffle(search)
        if search:
            return search[0]

        return {}


def format_tarot(tarot_card):
    """Formats the tarot card information into an embed."""
    title = f"**{tarot_card['name']}**"
    up_text = format_text(tarot_card["up"])
    down_text = format_text(tarot_card["down"])
    orientation = random.choice(
        [
            _("tarot_up_name"),
            _("tarot_down_name"),
        ]
    )
    description = (
        f"**{_('tarot_title')}** _({orientation})_"
        f"\n\n***{_('tarot_up_name')}***"
        f"\n> {up_text}"
        f"\n\n***{_('tarot_down_name')}***"
        f"\n> {down_text}"
    )
    footnote = (
        f"🖌{tarot_card['illustrator']}\n{tarot_card['set']} #{tarot_card['number']}."
    )
    embed = create_embed(title=title, description=description, footnote=footnote)

    return embed


tarot = Tarot()
