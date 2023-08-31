from interactions import Embed

from src.e_cards.formating import format_enemy_card, format_treachery_card, format_act_card_f, format_agenda_card_f, \
    format_location_card_f, format_scenario_card, format_general_card
from src.p_cards.formating import format_inv_card_f, format_player_card, format_customizable_upgrades


def resolve_search(r_cards) -> Embed:
    if r_cards:
        if r_cards[0]['type_code'] == "investigator":
            return format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            return format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            return format_treachery_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            return format_act_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            return format_agenda_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            return format_location_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            return format_scenario_card(r_cards[0])

        elif r_cards[0]['type_code'] in ['skill', 'event', 'asset']:
            return format_player_card(r_cards[0])
        else:
            return format_general_card(r_cards[0])


def resolve_customizable(r_cards) -> Embed:
    if r_cards:
        return format_customizable_upgrades(r_cards[0])