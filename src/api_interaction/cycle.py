import json

from config import LANG


class Cycle:
    """
    Class that handles the cycle data.
    """

    def __init__(self):
        with open(f"data/{LANG}/cycle.json", encoding="UTF-8") as f:
            self.cycle = json.load(f)

    def get_cycle_data(self):
        """Returns the cycle data from the JSON file.

        Returns:
            dict: The cycle data.
        """
        return self.cycle["cycles"]

    def get_cycle_name(self, code):
        """Returns the cycle name from the cycle code."""
        for c in self.cycle["cycles"]:
            if c["sufix"] == code[0:2]:
                return c["name"]
        return ""


cycle = Cycle()
