from src.api_interaction.taboo import taboo
from src.core.formatting import (
    format_text,
    format_name,
    format_subtext,
    format_faction,
    format_type,
    format_traits,
    format_card_text,
    format_flavour,
    format_illus_pack,
    create_embed,
    format_victory,
    format_vengeance,
)
from src.core.utils import text_if
from src.e_cards.formatting_utils import (
    format_enemy_stats,
    format_attack,
    format_clues,
    format_location_data,
)
from src.api_interaction.errata import errata
from src.core.translator import locale as _


def format_enemy_card(c):
    name = format_name(c)
    subtext = format_subtext(c)
    faction = format_faction(c)
    c_type = format_type(c)
    stats = format_enemy_stats(c)
    traits = text_if("%s\n", format_traits(c))
    text = text_if("> %s\n", format_card_text(c))
    flavour = text_if("%s\n\n", format_flavour(c))
    attack = text_if("%s\n", format_attack(c))
    victory = text_if("%s\n", format_victory(c))
    vengeance = text_if("%s\n", format_vengeance(c))
    errata_text = errata.format_errata_text(c["code"])

    taboo_text = taboo.format_taboo_text(c["code"])
    m_title = f"{faction} {name}{subtext}"
    m_description = (
        f"{c_type}\n"
        f"{stats}\n"
        f"{traits}\n"
        f"{text}"
        f"{victory}"
        f"{vengeance}"
        f"{attack}"
        f"{flavour}"
        f"{errata_text}"
        f"{taboo_text}"
    )
    m_footnote = format_illus_pack(c)
    return create_embed(m_title, m_description, c, m_footnote)


def format_act_card_f(c):
    name = format_name(c)
    stage = f"***{_('act')} {c['stage']}***"
    flavour = text_if("%s\n\n", format_flavour(c))
    clues = format_clues(c)
    text = text_if("> %s\n", format_card_text(c))
    errata_text = errata.format_errata_text(c["code"])

    m_title = name
    m_description = f"{stage}\n{flavour}{text}{clues}\n{errata_text}"
    m_footnote = format_illus_pack(c)
    return create_embed(m_title, m_description, c, m_footnote)


def format_agenda_card_f(c):
    name = format_name(c)
    stage = f"***{_('agenda')} {c['stage']}***"
    flavour = text_if("%s\n\n", format_flavour(c))
    text = text_if("> %s\n", format_card_text(c))
    errata_text = errata.format_errata_text(c["code"])
    doom = format_text("[doom] % s" % (c["doom"] if "doom" in c else " - "))

    m_title = name
    m_description = f"{stage}\n{flavour}{text}{doom}\n{errata_text}"
    m_footnote = format_illus_pack(c)
    return create_embed(m_title, m_description, c, m_footnote)


def format_location_card_f(c):
    name = format_name(c)
    c_type = format_type(c)
    subtext = format_subtext(c)
    traits = text_if("%s\n", format_traits(c))
    text = text_if("> %s\n", format_card_text(c))
    flavour = text_if("%s\n\n", format_flavour(c))
    location_data = format_location_data(c)
    victory = text_if("%s\n", format_victory(c))
    vengeance = text_if("%s\n", format_vengeance(c))
    errata_text = errata.format_errata_text(c["code"], back=True)

    m_title = f"{name}{subtext}"
    m_description = (
        f"{c_type}\n"
        f"{traits}\n"
        f"{location_data}\n"
        f"{text}\n"
        f"{victory}"
        f"{vengeance}\n"
        f"{flavour}"
        f"{errata_text}"
    )
    m_footnote = format_illus_pack(c)
    return create_embed(m_title, m_description, c, m_footnote)


def format_scenario_card(c):
    name = format_name(c)
    text = f"> {format_card_text(c)}"
    b_text = f"> {format_card_text(c, 'back_text')}"

    m_title = name
    m_description = f"{text}\n\n{b_text}"
    m_footnote = format_illus_pack(c)
    return create_embed(m_title, m_description, c, m_footnote)


def format_treachery_card(c):
    name = format_name(c)
    faction = format_faction(c)
    c_type = format_type(c)
    traits = format_traits(c)
    text = f"> {format_card_text(c)} \n"
    flavour = text_if("%s\n\n", format_flavour(c))
    errata_text = errata.format_errata_text(c["code"])
    victory = text_if("%s\n", format_victory(c))
    vengeance = text_if("%s\n", format_vengeance(c))
    m_title = f"{faction} {name}"
    taboo_text = taboo.format_taboo_text(c["code"])
    m_description = (
        f"{c_type}\n"
        f"{traits}\n\n"
        f"{text}\n"
        f"{victory}"
        f"{vengeance}"
        f"{flavour}"
        f"{errata_text}"
        f"{taboo_text}"
    )
    m_footnote = format_illus_pack(c)
    return create_embed(m_title, m_description, c, m_footnote)


def format_general_card(c):
    name = format_name(c)
    subname = format_subtext(c)
    text = format_card_text(c)
    flavour = text_if("%s\n\n", format_flavour(c))

    m_title = f"{name}{subname}"
    m_description = f"{flavour}{text}"
    m_footnote = format_illus_pack(c)
    embed = create_embed(m_title, m_description, c, m_footnote)
    return embed
