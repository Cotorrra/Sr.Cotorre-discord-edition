# Short cards
from src.core.formating import format_name, format_faction, format_text, format_victory
from src.e_cards.formating_utils import format_enemy_stats, format_attack, format_clues, extract_token_info


def format_enemy_card_short(c):
    formater = {"name": format_name(c),
                "faction": format_faction(c),
                "stats":  " [%s]" % format_enemy_stats(c),
                "attack": " [Atq: %s]" % format_attack(c) if format_attack(c) != "" else "",
                "victory": " [VP:%s]" % c['victory'] if "victory" in c else "",
                }

    text = "%(stats)s%(attack)s%(victory)s" % formater
    return text


def format_act_card_f_short(c):
    formater = {"name": format_name(c),
                "stage": "[A:%s]" % c['stage'],
                "clues": "[%s]" % format_clues(c),
                }

    text = "%(stage)s %(clues)s" % formater

    return text


def format_agenda_card_f_short(c):
    formater = {"name": format_name(c),
                "stage": "[P %s]" % c['stage'],
                "doom": format_text("[[doom] %s]" % (c['doom'] if "doom" in c else "-")),
                }
    text = "%(stage)s %(doom)s" % formater
    return text


def format_location_card_f_short(c):
    formater = {"name": format_name(c),
                "shroud": "[V: %s]" % str(c['shroud']),
                "clues": format_clues(c),
                "victory": format_victory(c),
                }
    text = "%(shroud)s %(clues)s %(victory)s" % formater
    return text


def format_scenario_card_short(c):
    formater = {"name": format_name(c),
                "text": "[F/N: %s]" % extract_token_info(c['text']),
                "b_text": "[D/E: %s]" % extract_token_info(c['back_text'])}

    text = "%(text)s %(b_text)s" % formater
    return text


def format_treachery_card_short(c):
    formater = {"name": format_name(c),
                "faction": format_faction(c)}

    text = "" % formater
    return text
