from core.formating import format_illus_pack
from e_cards.formating import format_enemy_card, format_treachery_card, format_act_card_f, format_agenda_card_f, \
    format_location_card_f, format_scenario_card, format_enemy_card_short, format_treachery_card_short, \
    format_act_card_f_short, format_agenda_card_f_short, format_scenario_card_short, format_location_card_f_short
from p_cards.formating import format_inv_card_f, format_player_card, format_inv_card_f_short, format_player_card_deck


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
        else:
            embed = format_player_card(r_cards[0])

        response = ""
        footing = format_illus_pack(r_cards[0])
        embed.set_footer(text=footing)


    else:
        response = "No encontré ninguna carta"
        embed = False

    return response, embed


def list_rest(array, max_entries=4):
    text = ""
    for c in array[1:max(max_entries, 1)]:
        if c['type_code'] == "investigator":
            text += "%s \n" % format_inv_card_f_short(c)

        elif c['type_code'] == "enemy":
            text += "%s \n" % format_enemy_card_short(c)

        elif c['type_code'] == "treachery":
            text += "%s \n" % format_treachery_card_short(c)

        elif c['type_code'] == 'act':
            text += "%s \n" % format_act_card_f_short(c)

        elif c['type_code'] == 'agenda':
            text += "%s \n" % format_agenda_card_f_short(c)

        elif c['type_code'] == 'location':
            text += "%s \n" % format_location_card_f_short(c)

        elif c['type_code'] == 'scenario':
            text += "%s \n" % format_scenario_card_short(c)
        else:
            text += format_player_card_deck(c, 1)[1:]
    return text
