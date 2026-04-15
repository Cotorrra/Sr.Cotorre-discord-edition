import json


class InvestigatorsTestHelper:
    """
    Helper class to load test data from JSON files.
    This class is used to load test data for investigators from a JSON file.
    """

    def __init__(self) -> None:
        with open("src/test/data/investigators.json", encoding="utf-8") as f:
            self.test_investigators = json.load(f)

    def get_investigators(self):
        """Get all investigators from the JSON file.

        Returns:
            list: A list of all investigators.
        """
        return self.test_investigators


class PlayerCardsTestHelper:
    """
    Helper class to load test data from JSON files.
    This class is used to load test data for cards from a JSON file.
    """

    def __init__(self) -> None:
        with open("src/test/data/p_cards.json", encoding="utf-8") as f:
            self.p_cards = json.load(f)

    def get_all_cards(self):
        """Get all cards from the JSON file.

        Returns:
            list: A list of all cards.
        """
        return self.p_cards


class EncounterCardsTestHelper:
    """
    Helper class to load test data from JSON files.
    This class is used to load test data for encounter cards from a JSON file.
    """

    def __init__(self) -> None:
        with open("src/test/data/e_cards.json", encoding="utf-8") as f:
            self.e_cards = json.load(f)

    def get_all_cards(self):
        """Get all cards from the JSON file.

        Returns:
            list: A list of all cards.
        """
        return self.e_cards
