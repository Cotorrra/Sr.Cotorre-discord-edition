from src.core.formating import format_number, format_victory, format_text
from src.p_cards.utils import format_slot, format_skill_icons, format_health_sanity, format_inv_skills


def format_player_card_short(c):
    formater = {"type": "[%s" % c['type_name'],
                "slot": ": %s]" % format_slot(c) if format_slot(c) else "]",
                "icons": "[I: %s]" % format_skill_icons(c) if format_skill_icons(c) != "" else "",
                "costs": "[C: %s]" % format_number(c['cost']) if "cost" in c else "",
                "health_sanity": "[%s]" % format_health_sanity(c) if format_health_sanity(c) != "" else "",
                "victory": "[VP:%s]" % format_victory(c) if format_victory(c) else "",
                }
    text = "%(type)s%(slot)s%(costs)s%(icons)s%(health_sanity)s%(victory)s" % formater
    return text


def format_inv_card_f_short(c):
    formater = {"class": format_text("[%s]" % c['faction_code']),
                "name": "%s" % c['name'],
                "skills": format_inv_skills(c),
                "health_sanity": format_text("%s%s" % ("[health] %s " % c['health'], "[sanity] %s" % c['sanity'])),
                }
    text = "[%(skills)s][%(health_sanity)s]" % formater
    return text
