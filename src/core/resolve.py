from src.e_cards.formating import format_enemy_card, format_treachery_card, format_act_card_f, format_agenda_card_f, \
    format_location_card_f, format_scenario_card, format_general_card
from src.p_cards.formating import format_inv_card_f, format_player_card


def resolve_search(r_cards):
    if r_cards:
        if r_cards[0]['type_code'] == "investigator":
            embed = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            embed = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            embed = format_treachery_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            embed = format_act_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            embed = format_agenda_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            embed = format_location_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            embed = format_scenario_card(r_cards[0])

        elif r_cards[0]['type_code'] in ['skill', 'event', 'asset']:
            embed = format_player_card(r_cards[0])
        else:
            embed = format_general_card(r_cards[0])
    else:
        embed = False

    return embed

