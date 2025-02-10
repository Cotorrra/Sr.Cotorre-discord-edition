from interactions import Embed

from src.e_cards.formating import (
    format_act_card_f,
    format_agenda_card_f,
    format_enemy_card,
    format_general_card,
    format_location_card_f,
    format_scenario_card,
    format_treachery_card,
)
from src.p_cards.formatting import (
    format_customizable_upgrades,
    format_inv_card_f,
    format_player_card,
)


def resolve_search(r_cards) -> Embed:
    """Resolves the search results into an embed."""
    match r_cards[0]["type_code"]:
        case "investigator":
            resolve_function = format_inv_card_f
        case "enemy":
            resolve_function = format_enemy_card
        case "treachery":
            resolve_function = format_treachery_card
        case "act":
            resolve_function = format_act_card_f
        case "agenda":
            resolve_function = format_agenda_card_f
        case "location":
            resolve_function = format_location_card_f
        case "scenario":
            resolve_function = format_scenario_card
        case "skill" | "event" | "asset":
            resolve_function = format_player_card
        case _:
            resolve_function = format_general_card
    print(resolve_function.__name__)
    return resolve_function(r_cards[0])


def resolve_customizable(r_cards) -> Embed:
    """Resolves the search results into an embed."""
    return format_customizable_upgrades(r_cards[0])
