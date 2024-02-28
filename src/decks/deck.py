from ast import literal_eval

from src.core.search import find_by_id
from src.p_cards.utils import cos_info_to_dict, get_color_by_investigator
from src.api_interaction.taboo import taboo


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
        for _ in range(qty):
            arr_deck.append(find_by_id(c_id, cards))
    return arr_deck


def check_upgrade_rules(deck1, deck2, cards):
    info = {"buys_in": [], "buys_out": [],
            "xp_diff": 0, "xp_spent": 0,
            "color": get_color_by_investigator(deck1, cards),
            "taboo_id": "00" + str(deck1['taboo_id']) if deck1['taboo_id'] else "000",
            "cuz_upgrades_in": {}, "cuz_upgrades_cards": []
            }
    a_deck1 = deck_to_array(deck1, cards)
    a_deck2 = deck_to_array(deck2, cards)
    info["buys_out"], info["buys_in"] = diff_decks(a_deck1, a_deck2)
    if 'meta' in deck1 and 'meta' in deck2:
        info["cuz_upgrades_in"], info["cuz_upgrades_cards"] = diff_customizable(deck1['meta'], deck2['meta'], cards)
    info["xp_diff"] = deck2['xp'] if "xp" in deck2 else 0
    info["xp_spent"] = deck2['xp_spent'] if 'xp_spent' in deck2 else 0

    return info

def diff_customizable(meta1, meta2, cards):
    """
    Returns the differences between the customizable cards info of the decks
    Always upgrading from deck1 to deck2
    """
    diff = {}
    card_list = []
    meta_1 = literal_eval(meta1)
    meta_2 = literal_eval(meta2)
    meta_1_dict = cos_info_to_dict(meta_1, cards)
    meta_2_dict = cos_info_to_dict(meta_2, cards)
    
    for card_id, upgrades in meta_2_dict.items():
        if card_id not in meta_1_dict:
            # If the key is not in the first meta, it means that the upgrade is all the 2nd meta
            diff[card_id] = upgrades
            card_list.append(find_by_id(card_id, cards))
        else:
            # This is a string comparison c:
            if meta_1[f"cus_{card_id}"] != meta_2[f"cus_{card_id}"]:
                # If the values not are the same, it means that was an upgrade
                upgrades_diff = {}
                for upgrade_id, upgrade_info in upgrades.items():
                    if upgrade_id not in meta_1_dict[card_id]:
                        upgrades_diff[upgrade_id] = upgrade_info
                    else:
                        xp_diff = int(upgrade_info["xp"]) - int(meta_1_dict[card_id][upgrade_id]["xp"])
                        if xp_diff > 0:
                            upgrades_diff[upgrade_id] = {}
                            upgrades_diff[upgrade_id]["xp"] = xp_diff
                            if "info" in upgrade_info:
                                upgrades_diff[upgrade_id]["info"] = upgrade_info["info"]
                if upgrades_diff:
                    diff[card_id] = upgrades_diff
                    card_list.append(find_by_id(card_id, cards))
    return diff, card_list

def extract_deck_info(deck, cards):
    deck_meta = cos_info_to_dict(literal_eval(deck['meta']), cards)
    # literal_eval(deck['meta'])
    info = {"assets": [],
            "assets_permanents": [], "events": [], "skills": [], "treachery": [],
            "assets_q": 0, "events_q": 0, "skills_q": 0, "treachery_q": 0, "assets_permanents_q": 0,
            "xp": 0, "color": get_color_by_investigator(deck, cards),
            "taboo_id": "00" + str(deck['taboo_id']) if deck['taboo_id'] else "000",
            'deck_meta': deck_meta
            }
    for c_id, qty in deck['slots'].items():
        card = find_by_id(c_id, cards)
        text = (card, qty)
        info["xp"] += taboo.calculate_xp(card, qty, info['taboo_id'], deck_meta)

        if 'real_text' in card and 'Permanent.' in card['real_text']:
            info['assets_permanents'].append(text)
            info['assets_permanents_q'] += qty

        elif card['type_code'] == "asset":
            info['assets_q'] += qty
            info['assets'].append(text)

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

