from src.core.formating import format_text, format_number, color_picker
from src.core.search import find_by_id
from src.core.translator import lang

def format_slot(c):
    formater = {
        "Accessory.": "<:accessory:923314322606788639>",
        "Ally.": "<:ally:923314296727941132>",
        "Arcane.": "<:arcane:923314241904214077>",
        "Arcane x2.": "<:2arcane:923314267300696104>",
        "Body.": "<:body:923314103970316308>",
        "Hand.": "<:hand:923314022428844072>",
        "Hand x2.": "<:2hand:923314070227124225> ",
        "Tarot.": "<:tarot:923313991839805520>"
    }
    text = ""
    if "real_slot" in c:
        for key, value in formater.items():
            traits = c["real_slot"] + "."
            if key in traits:
                text += value

    return text


def format_inv_skills(c):
    will = f"{c['skill_willpower']} [willpower]" if "skill_willpower" in c else ""
    intel = f"{c['skill_intellect']} [intellect]" if "skill_intellect" in c else ""
    com = f"{c['skill_combat']} [combat]" if "skill_combat" in c else ""
    agi = f"{c['skill_agility']} [agility]" if "skill_agility" in c else ""
    return format_text(f"{will} {intel} {com} {agi}")


def format_skill_icons(c):
    will = f"{c['skill_willpower']*'[willpower]'}" if "skill_willpower" in c else ""
    intel = f"{c['skill_intellect']*'[intellect]'}" if "skill_intellect" in c else ""
    com = f"{c['skill_combat']*'[combat]'}" if "skill_combat" in c else ""
    agi = f"{c['skill_agility']*'[agility]'}" if "skill_agility" in c else ""
    wild = f"{c['skill_wild']*'[wild]'}" if "skill_wild" in c else ""
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
            if ("Campaign Log" in c['real_text'] or
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
