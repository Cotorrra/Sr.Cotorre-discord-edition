from src.core.formating import *


def format_enemy_stats(c):
    formater = {"health": "[health]: %s%s " % (format_number(c['health']) if "health" in c else "-",
                                               "[per_investigator]" if c["health_per_investigator"] else ""),
                "combat": "[combat]: %s " % (format_number(c['enemy_fight']) if "enemy_fight" in c else "-"),
                "agility": "[agility]: %s" % (format_number(c['enemy_evade']) if "enemy_evade" in c else "-")
                }

    return format_text("%(combat)s  %(health)s  %(agility)s" % formater)


def format_clues(c):
    if "clues" in c:
        clues = str(c['clues'])
        if 'clues_fixed' in c or c['clues'] == 0:
            return format_text("Pistas: %s" % clues)
        else:
            return format_text("Pistas: %s [per_investigator]" % clues)
    else:
        return format_text("Pistas: -")


def format_location_data(c):
    formater = {"shroud": "Velo: %s" % str(c['shroud']),
                "clues": format_clues(c)}
    return "%(shroud)s\n%(clues)s \n" % formater


def format_attack(c):
    formater = {
        "damage": "[health]" * c['enemy_damage'] if "enemy_damage" in c else "",
        "horror": "[sanity]" * c['enemy_horror'] if "enemy_horror" in c else "",
    }
    return format_text("%(damage)s%(horror)s" % formater)


def extract_token_info(t):
    lines = t.split("\n")
    symbols = ["", "", "", ""]  # Skull / Cultist / Tablet / Elder
    for line in lines:
        if "[skull]" in line:
            symbols[0] = "[skull]: %s " + line.split(": ")[1][:2]
        if "[cultist]" in line:
            symbols[1] = "[cultist]: %s " + line.split(": ")[1][:2]
        if "[tablet]" in line:
            symbols[2] = "[tablet]: %s " + line.split(": ")[1][:2]
        if "[elder_thing]" in line:
            symbols[3] = "[elder_thing]: %s " + line.split(": ")[1][:2]

    text = "["
    for s in symbols:
        if s:
            text += s
    text += "]"
    return format_text(text)
