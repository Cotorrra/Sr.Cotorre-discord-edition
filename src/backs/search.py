from src.backs.formatting import (
    format_general_card_b,
    format_inv_card_b,
    format_location_card_b,
)
from src.e_cards.formating import format_scenario_card
from src.p_cards.formatting import format_player_card


def resolve_back_search(r_cards):
    """Resolves the search results into an embed."""
    match r_cards[0]["type_code"]:
        case "investigator":
            resolve_function = format_inv_card_b
        case "location":
            resolve_function = format_location_card_b
        case "scenario":
            resolve_function = format_scenario_card
        case "skill" | "event" | "asset":
            resolve_function = format_player_card
        case _:  # Enemy, Act, Agenda, Treachery goes here
            resolve_function = format_general_card_b
    return resolve_function(r_cards[0])
