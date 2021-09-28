from src.core.formating import format_text, format_number, color_picker
from src.core.search import find_by_id
from src.core.translator import locale


def format_xp(c):
    if "xp" in c:
        if c['xp'] == 0:
            text = ""
        elif c['exceptional']:
            text = " (%sE)" % c['xp']
        else:
            text = " (%s)" % c['xp']
    else:
        text = ""
    return text


def format_slot(c):
    formater = {
        "Accessory.": "<:Accesorio:813546875856355359>",
        "Ally.": "<:Aliado:813546887989821472>",
        "Arcane.": "<:huecoarcano:813551281791959040>",
        "Arcane x2.": "<:Dosarcanos:813552984432050186>",
        "Body.": "<:Cuerpo:813546864074162226>",
        "Hand.": "<:Mano:813546904428347402>",
        "Hand x2.": "<:Dosmanos:813546852083302460>",
        "Tarot.": "<:Tarot:813551294156767232>"
    }
    text = ""
    if "real_slot" in c:
        for key, value in formater.items():
            traits = c["real_slot"] + "."
            if key in traits:
                text += value

    return text


def format_inv_skills(c):
    formater = {
        "will": "[willpower] %s " % c['skill_willpower'] if "skill_willpower" in c else "",
        "int": "[intellect] %s " % c['skill_intellect'] if "skill_intellect" in c else "",
        "com": "[combat] %s " % c['skill_combat'] if "skill_combat" in c else "",
        "agi": "[agility] %s" % c['skill_agility'] if "skill_agility" in c else "",
    }
    return format_text("%(will)s%(int)s%(com)s%(agi)s" % formater)


def format_skill_icons(c):
    formater = {
        "will": "[willpower]" * c['skill_willpower'] if "skill_willpower" in c else "",
        "int": "[intellect]" * c['skill_intellect'] if "skill_intellect" in c else "",
        "com": "[combat]" * c['skill_combat'] if "skill_combat" in c else "",
        "agi": "[agility]" * c['skill_agility'] if "skill_agility" in c else "",
        "wild": "[wild]" * c['skill_wild'] if "skill_wild" in c else "",
    }
    return format_text("%(will)s%(int)s%(com)s%(agi)s%(wild)s" % formater)


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
        return f"{locale('cost')}: %s \n" % format_number(c['cost'])
    else:
        return ""