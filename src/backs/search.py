from src.backs.formating import format_general_card_b, format_location_card_b, format_inv_card_b
from src.e_cards.formating import format_scenario_card
from src.p_cards.formating import format_player_card


def resolve_back_search(r_cards):
    if r_cards:
        if r_cards[0]['type_code'] == "investigator":
            embed = format_inv_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            embed = format_general_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            embed = format_location_card_b(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            embed = format_scenario_card(r_cards[0])
        else:
            embed = format_player_card(r_cards[0])
    else:
        embed = False

    return embed

