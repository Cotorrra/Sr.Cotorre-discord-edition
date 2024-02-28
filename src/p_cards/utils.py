import re

from src.core.formating import format_text, format_number, color_picker
from src.core.search import find_by_id
from src.core.translator import lang


def format_slot(c):
    formater = {
        "Accessory": "<:accessory:923314322606788639>",
        "Ally": "<:ally:923314296727941132>",
        "Arcane": "<:arcane:923314241904214077>",
        "Arcane x2": "<:2arcane:923314267300696104>",
        "Body": "<:body:923314103970316308>",
        "Hand": "<:hand:923314022428844072>",
        "Hand x2": "<:2hand:923314070227124225> ",
        "Tarot": "<:tarot:923313991839805520>"
    }
    text = ""
    if "real_slot" in c:
        if c["real_slot"]:
            slots = c["real_slot"].split(". ")
            for slot in slots:
                text += formater[slot]
    elif "slot" in c:
        if c["slot"]:
            slots = c["slot"].split(". ")
            for slot in slots:
                text += formater[slot]

    return text


def format_inv_skills(c):
    will = f"{c['skill_willpower']} [willpower]" if "skill_willpower" in c else ""
    intel = f"{c['skill_intellect']} [intellect]" if "skill_intellect" in c else ""
    com = f"{c['skill_combat']} [combat]" if "skill_combat" in c else ""
    agi = f"{c['skill_agility']} [agility]" if "skill_agility" in c else ""
    return format_text(f"{will} {intel} {com} {agi}")


def format_skill_icons(c):
    will = f"{c['skill_willpower'] * '[willpower]'}" if "skill_willpower" in c else ""
    intel = f"{c['skill_intellect'] * '[intellect]'}" if "skill_intellect" in c else ""
    com = f"{c['skill_combat'] * '[combat]'}" if "skill_combat" in c else ""
    agi = f"{c['skill_agility'] * '[agility]'}" if "skill_agility" in c else ""
    wild = f"{c['skill_wild'] * '[wild]'}" if "skill_wild" in c else ""
    return format_text(f"{will}{intel}{com}{agi}{wild}")


def format_health_sanity(c):
    return format_text("%s%s" % ("[health] %s " % format_number(c['health']) if "health" in c else "",
                                 "[sanity] %s" % format_number(c['sanity']) if "sanity" in c else ""))


def get_color_by_investigator(deck, cards):
    inv_id = deck['investigator_code']
    inv_card = find_by_id(inv_id, cards)
    return color_picker(inv_card)


def format_sub_text_short(c):
    if 'real_text' in c:
        if "subname" in c:
            if ("Researched." in c['real_text'] or
                    "Directive" in c['real_name'] or
                    "Discipline" in c['real_name']):
                return f": _{c['subname']}_"
        if 'Advanced.' in c['real_text']:
            return f" _(Adv)_"
    return ""


def format_costs(c):
    if "cost" in c:
        return f"{lang.locale('cost')}: %s \n" % format_number(c['cost'])
    else:
        return ""


def extract_upgrades_names(c) -> list:
    """
        Extracts the names of upgrades from a customizable card.

        Args:
            c (dict): A card dict

        Returns:
            list: A list of upgrade names.
    """
    if 'customization_text' in c:
        upgrade_regex = r"□+ <b>(.*)\.</b>"
        upgrade_list = c['customization_text'].split("\n")
        upgrades_names = []
        for upgrade in upgrade_list:
            if re.findall(upgrade_regex, upgrade):
                upgrades_names.append(re.findall(upgrade_regex, upgrade)[0])
            else:
                upgrades_names.append("")
        return upgrades_names
        
    return []


def format_customizable_note(c: dict) -> str:
    """
    Format the costumization upgrades, if any.
    :param c:
    :return:
    """

    if "customization_text" in c:
        return f"_{lang.locale('customization_note')}_\n"

    return ""


def format_customizable(c: dict) -> str:
    """
    Format the costumization upgrades, if any.
    :param c:
    :return:
    """

    if "customization_text" in c:
        return f"{format_text(c['customization_text'])}\n"

    return ""


def customize_card(card: dict, deck_meta={}) -> dict:
    """
    Customizes a card with the given deck meta.

    Args:
        card (dict): A card dict
        deck_meta (dict): A deck meta dict

    Returns:
        dict: A card dict
    """
    c = card.copy()
    if card['code'] in ['09021', '09079', '09080'] and card['code'] in deck_meta:
        card_meta = deck_meta[card['code']]
        for upgrade_id, upgrade_info in card_meta.items():
            # Here you can add the customization rules for each card when Needed
                if card['code'] == '09021' and upgrade_id == '0' and upgrade_info['xp'] == '1':
                    # Hunter's Armor: Enchanted
                    c['real_slot'] = "Arcane"
                if card['code'] == '09079' and upgrade_id == '3' and upgrade_info['xp'] == '2':
                    # Living Ink: Imbued Ink
                    c['real_slot'] = "Arcane"
                if card['code'] == '09080' and upgrade_id == '5' and upgrade_info['xp'] == '2':
                    # Summoned Servitor: Dominance
                    if upgrade_info['info'] == '0':
                        c['real_slot'] = "Arcane"
                    elif upgrade_info['info'] == '1':
                        c['real_slot'] = "Ally"
    return c

def cos_info_to_dict(meta={}, cards={}) -> dict:
    """
    Converts the costumization info to a dict.

    Args:
        meta (str): The costumization info

    Returns:
        dict: The costumization info as a dict
    Example: 
    >>> meta = {
        "cus_09021": "0|1|Enchanted",
        "cus_09079": "3|2|Imbued Ink,1|1",
        "cus_09080": "5|2|Dominance,2|2,3|3"
    }
    >>> cos_info_to_dict(meta)
    {
        "09021": {
            "0": {
                "xp": "1",
                "info": "Enchanted"
            }
        },
        "09079": {
            "3": {
                "xp": "2",
                "info": "Imbued Ink"
            },
            "1": {
                "xp": "1"
            }
        },
        "09080": {
            "5": {
                "xp": "2",
                "info": "Dominance"
            },
            "2": {
                "xp": "2"
            },
            "3": {
                "xp": "3"
            }
        }
    }
    """
    info = {}
    for key, value in meta.items():
        key_info = {}
        if key.startswith("cus_"):
            values = value.split(",")
            for v in values:
                chain = v.split("|")
                if int(chain[1]) > 0 or (key in ['cus_09042', 'cus_09060', 'cus_09079', 'cus_09101'] and chain[0] == '0'):
                    key_info[chain[0]] = {}
                    key_info[chain[0]]['xp'] = chain[1]
                    if len(chain) > 2:
                        if key == 'cus_09042' and chain[0] in ['0', '4']:
                            info_text = ""
                            for id in chain[2].split("^"):
                                info_text += find_by_id(id, cards)['name'] + "+"
                            key_info[chain[0]]['info'] = info_text[:-1]
                        else:
                            key_info[chain[0]]['info'] = chain[2]
        # key[4:] removes the "cus_" prefix
        info[key[4:]] = key_info
    return info