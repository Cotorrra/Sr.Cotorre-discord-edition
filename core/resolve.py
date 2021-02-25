from core.formating import format_illus_pack
from e_cards.formating import format_enemy_card, format_treachery_card, format_act_card_f, format_agenda_card_f, \
    format_location_card_f, format_scenario_card, format_enemy_card_short, format_treachery_card_short, \
    format_act_card_f_short, format_agenda_card_f_short, format_scenario_card_short, format_location_card_short
from p_cards.formating import format_inv_card_f, format_player_card, format_inv_card_f_short, format_player_card_short


def resolve_search(r_cards):
    if r_cards:
        if r_cards[0]['type_code'] == "investigator":
            response = "¡Carta de Investigador encontrada!"
            embed = format_inv_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == "enemy":
            response = "¡Carta de Enemigo encontrada!"
            embed = format_enemy_card(r_cards[0])

        elif r_cards[0]['type_code'] == "treachery":
            response = "¡Carta de Traición encontrada!"
            embed = format_treachery_card(r_cards[0])

        elif r_cards[0]['type_code'] == 'act':
            response = "¡Carta de Acto encontrada!"
            embed = format_act_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'agenda':
            response = "¡Carta de Plan encontrada!"
            embed = format_agenda_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'location':
            response = "¡Carta de Lugar encontrada!"
            embed = format_location_card_f(r_cards[0])

        elif r_cards[0]['type_code'] == 'scenario':
            response = "¡Carta de Escenario encontrada!"
            embed = format_scenario_card(r_cards[0])
        else:
            response = "¡Carta de Jugador encontrada!"
            embed = format_player_card(r_cards[0])

        footing = format_illus_pack(r_cards[0])

        if len(r_cards) > 1:
            footing += "" # "\n Encontré otras cartas más: \n%s" % list_rest(r_cards)
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
            text += "%s \n" % format_location_card_short(c)

        elif c['type_code'] == 'scenario':
            text += "%s \n" % format_scenario_card_short(c)
        else:
            text += format_player_card_short(c, 1)[1:]
    return text
