from src.core.search import find_by_id
from src.p_cards.utils import get_color_by_investigator
from src.taboo.taboo import taboo_data


def diff_decks(a_deck1, a_deck2):
    """
    Returns a tuple with the differences of the decks given:
    - The first element contains the cards that are in the 2nd deck but not in the 1st.
    - The second element contains the cards that are in the 1st deck but not in the 2nd.
    :param a_deck1:
    :param a_deck2:
    :return:
    """

    d_out = a_deck1.copy()
    d_in = a_deck2.copy()
    for c in a_deck1:
        if c in d_in:
            d_out.remove(c)
            d_in.remove(c)
    return d_out, d_in


def deck_to_array(deck, cards):
    arr_deck = []
    for c_id, qty in deck['slots'].items():
        for i in range(qty):
            arr_deck.append(find_by_id(c_id, cards))
    return arr_deck


def check_upgrade_rules(deck1, deck2, cards):
    info = {"buys_in": [], "buys_out": [],
            "xp_diff": 0, "color": get_color_by_investigator(deck1, cards)}
    a_deck1 = deck_to_array(deck1, cards)
    a_deck2 = deck_to_array(deck2, cards)
    info["buys_out"], info["buys_in"] = diff_decks(a_deck1, a_deck2)
    info["xp_diff"] = deck2['xp'] if "xp" in deck2 else 0

    return info


def extract_deck_info(deck, cards):
    info = {"assets_others": [], "assets_hand": [], "assets_hand2": [], "assets_body": [],
            "assets_accessory": [], "assets_arcane": [], "assets_arcane2": [], "assets_ally": [],
            "assets_permanents": [], "events": [], "skills": [], "treachery": [],
            "assets_q": 0, "events_q": 0, "skills_q": 0, "treachery_q": 0, "assets_permanents_q": 0,
            "xp": 0, "color": get_color_by_investigator(deck, cards)}
    taboo_version = "00" + str(deck['taboo_id'])
    for c_id, qty in deck['slots'].items():
        card = find_by_id(c_id, cards)
        text = (card, qty)
        info["xp"] += taboo_data.calculate_xp(card, qty, taboo_version)

        if 'Permanent.' in card['real_text']:
            info['assets_permanents'].append(text)
            info['assets_permanents_q'] += qty

        elif card['type_code'] == "asset":
            info['assets_q'] += qty
            if 'real_slot' in card:
                if card['real_slot'] == 'Hand':
                    info['assets_hand'].append(text)

                elif card['real_slot'] == 'Hand x2':
                    info['assets_hand2'].append(text)

                elif card['real_slot'] == 'Arcane':
                    info['assets_arcane'].append(text)

                elif card['real_slot'] == 'Arcane x2':
                    info['assets_arcane2'].append(text)

                elif card['real_slot'] == 'Accessory':
                    info['assets_accessory'].append(text)

                elif card['real_slot'] == 'Body':
                    info['assets_body'].append(text)

                elif card['real_slot'] == 'Ally':
                    info['assets_ally'].append(text)
                else:
                    info['assets_others'].append(text)
            else:
                info['assets_others'].append(text)

        elif card['type_code'] == "event":
            info['events'].append(text)
            info['events_q'] += qty

        elif card['type_code'] == "skill":
            info['skills'].append(text)
            info['skills_q'] += qty
        else:
            info['treachery'].append(text)
            info['treachery_q'] += qty

    return info

