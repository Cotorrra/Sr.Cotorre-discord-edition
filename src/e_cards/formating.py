from src.core.formating import *
from src.e_cards.formating_utils import format_enemy_stats, format_attack, format_clues, \
    format_location_data
from src.errata.formating import format_errata_text


def format_enemy_card(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "type": "***%s***\n" % c['type_name'],
                "traits": "*%s*\n" % c['traits'] if "traits" in c else "",
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n\n" % format_text(c['flavor']) if "flavor" in c else "",
                "stats": "%s \n" % format_enemy_stats(c),
                "attack": "Ataque: %s\n" % format_attack(c) if format_attack(c) != "" else "",
                "victory": format_victory(c),
                "vengeance": format_vengeance(c),
                "errata_text": format_errata_text(c['code']),
                }

    m_title = " %(faction)s %(name)s%(subtext)s" % formater
    m_description = "%(type)s" \
                    "%(traits)s" \
                    "%(stats)s\n" \
                    "%(text)s" \
                    "%(victory)s" \
                    "%(vengeance)s\n" \
                    "%(attack)s\n" \
                    "%(flavour)s" \
                    "%(errata_text)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_act_card_f(c):
    formater = {"name": format_name(c),
                "stage": "***Acto %s***\n" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "clues": "%s\n" % format_clues(c),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "errata_text": format_errata_text(c['code']),
                }

    m_title = "%(name)s " % formater
    m_description = "%(stage)s" \
                    "%(clues)s\n" \
                    "%(flavour)s" \
                    "%(text)s \n" \
                    "%(errata_text)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_agenda_card_f(c):
    formater = {"name": format_name(c),
                "stage": "***Plan %s***\n" % c['stage'],
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "doom": format_text("[doom] %s" % (c['doom'] if "doom" in c else "-")),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "errata_text":  format_errata_text(c['code']),
                }

    m_title = "%(name)s " % formater
    m_description = "%(stage)s" \
                    "%(doom)s\n" \
                    "%(flavour)s" \
                    "%(text)s\n" \
                    "%(errata_text)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_location_card_f(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "traits": "*%s*\n" % c['traits'] if "traits" in c else "",
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "location_data": format_location_data(c),
                "victory": format_victory(c),
                "vengeance": format_vengeance(c),
                "errata_text": format_errata_text(c['code'], back=True),
                }
    m_title = "%(name)s%(subtext)s" % formater
    m_description = "%(traits)s" \
                    "%(location_data)s" \
                    "%(text)s" \
                    "%(victory)s" \
                    "%(vengeance)s\n" \
                    "%(flavour)s \n" \
                    "%(errata_text)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_scenario_card(c):
    formater = {"name": format_name(c),
                "text": "> %s \n" % format_text(c['text']),
                "b_text": "> %s \n" % format_text(c['back_text']),
                "pack": format_set(c)}

    m_title = "%(name)s" % formater
    m_description = "%(text)s \n" \
                    "%(b_text)s \n" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_treachery_card(c):
    formater = {"name": format_name(c),
                "faction": format_faction(c),
                "type": "***%s***\n" % c['type_name'],
                "traits": "*%s*\n" % c['traits'] if "traits" in c else "",
                "text": "> %s \n" % format_card_text(c),
                "flavour": "_%s_\n" % format_text(c['flavor']) if "flavor" in c else "",
                "errata_text": format_errata_text(c['code'], back=True),
                }

    m_title = "%(faction)s %(name)s" % formater
    m_description = "%(type)s" \
                    "%(traits)s \n" \
                    "%(text)s \n" \
                    "%(flavour)s \n" \
                    "%(errata_text)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_general_card(c):
    formater = {"name": format_name(c),
                "subname": format_subtext(c),
                "text": "%s \n" % format_card_text(c, "text") if "text" in c else "",
                "pack": format_set(c),
                "flavour": format_text("<i>%s</i>\n" % c['flavor'] if "flavor" in c else ""),
                }
    m_title = "%(name)s %(subname)s" % formater
    m_description = "%(flavour)s \n" \
                    "%(text)s" % formater
    m_footnote = "%(pack)s" % formater
    embed = create_embed(c, m_title, m_description, m_footnote)
    return embed
