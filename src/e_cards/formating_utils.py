from src.core.formating import *


def format_enemy_stats(c):
    health = "[health] %s%s" % (format_number(c['health']) if "health" in c else "-",
                                "[per_investigator]" if c["health_per_investigator"] else "")
    combat = "[combat] %s" % (format_number(c['enemy_fight']) if "enemy_fight" in c else "-")
    agility = "[agility] %s" % (format_number(c['enemy_evade']) if "enemy_evade" in c else "-")

    return format_text(f"{combat} / {health} / {agility}")


def format_clues(c):
    if "clues" in c:
        clues = str(c['clues'])
        if 'clues_fixed' in c or c['clues'] == 0:
            return format_text(f"[clues] {clues}")
        else:
            return format_text(f"[clues] {clues} [per_investigator]")
    else:
        return format_text(f"[clues] -")


def format_location_data(c):
    shroud = f"{lang.locale('shroud')}: {str(c['shroud'])}"
    clues = format_clues(c)
    return f"{shroud} / {clues}"


def format_attack(c, verbose=True):
    damage = ""
    if "enemy_damage" in c:
        damage = format_text("[health]" * c['enemy_damage'])
    horror = ""
    if "enemy_horror" in c:
        horror = format_text("[sanity]" * c['enemy_horror'])

    if not damage and not horror:
        return ""
    elif verbose:
        return f"{lang.locale('attack')}: {damage}{horror}\n"
    else:
        return f"{damage}{horror}\n"


def extract_token_info(t):
    lines = t.split("\n")
    symbols = ["", "", "", ""]  # Skull / Cultist / Tablet / Elder
    for line in lines:
        if "[skull]" in line:
            symbols[0] = f"[skull]: {line.split(': ')[1][:2]}"
        if "[cultist]" in line:
            symbols[1] = f"[cultist]: {line.split(': ')[1][:2]}"
        if "[tablet]" in line:
            symbols[2] = f"[tablet]: {line.split(': ')[1][:2]}"
        if "[elder_thing]" in line:
            symbols[3] = f"[elder_thing]: {line.split(': ')[1][:2]}"

    text = "["
    for s in symbols:
        if s:
            text += s
    text += "]"
    return format_text(text)
