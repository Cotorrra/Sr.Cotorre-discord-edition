import json

from config import LANG
from src.core.formatting import format_text, create_embed


class Timings:
    """Class that handles the timing data from the data/timings.json file."""

    def __init__(self):
        with open(f"data/{LANG}/timings.json", encoding="UTF-8") as f:
            self.timings = json.load(f)

    def get_timings_data(self):
        """Returns the timings data from the JSON file."""
        return self.timings

    def find_formatted_timing(self, query):
        """Formats the timing information into an embed."""
        timing = self.timings["framework"][query]
        name, text = next(iter(timing.items()))
        title = f"**{name}**"
        description = ">>> "
        for line in text:
            description += f"{format_text(line)}\n"
        embed = create_embed(title=title, description=description)
        return embed


timings = Timings()
