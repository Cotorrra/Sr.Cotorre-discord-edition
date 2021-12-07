from src.core.formating import format_name, format_subtext, format_faction, format_card_text, \
    faction_order, format_victory, format_illus_pack, create_embed, format_flavour, format_type, format_traits
from src.core.utils import text_if
from src.errata.formating import format_errata_text
from src.p_cards.utils import format_xp, format_slot, format_skill_icons, format_health_sanity, format_inv_skills, \
    format_sub_text_short, format_costs
from src.taboo.formating import format_taboo_text


def format_player_card(c):
    name = format_name(c)
    level = format_xp(c)
    subtext = format_subtext(c)
    faction = format_faction(c)
    type = format_type(c)
    slot = format_slot(c)

    traits = text_if("%s\n", format_traits(c))
    icons = text_if("%s\n", format_skill_icons(c))
    costs = format_costs(c)

    text = text_if("> %s\n", format_card_text(c))
    flavour = text_if("%s\n", format_flavour(c))
    health_sanity = text_if("%s\n", format_health_sanity(c))
    taboo_text = format_taboo_text(c['code'])
    errata_text = format_errata_text(c['code'])
    victory = text_if("> %s\n", format_victory(c))

    m_title = f"{faction} {name}{subtext}{level}"
    m_description = f"{type} {slot}\n" \
                    f"{traits}" \
                    f"{costs}" \
                    f"{icons}\n" \
                    f"{text}" \
                    f"{victory}" \
                    f"{health_sanity}\n" \
                    f"{flavour}" \
                    f"{errata_text}" \
                    f"{taboo_text}"
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_inv_card_f(c):
    faction = format_faction(c)
    name = format_name(c)
    subname = format_subtext(c)
    skills = format_inv_skills(c)
    health_sanity = text_if("%s\n", format_health_sanity(c))
    ability = text_if("> %s", format_card_text(c))
    traits = format_traits(c)
    taboo_text = format_taboo_text(c['code'])
    errata_text = format_errata_text(c['code'])
    flavour = format_flavour(c)

    m_title = f"{faction} {name}{subname}"
    m_description = f"{skills}\n" \
                    f"{traits}\n\n" \
                    f"{ability}\n" \
                    f"{health_sanity}\n" \
                    f"{flavour}\n" \
                    f"{errata_text}\n" \
                    f"{taboo_text}\n"
    m_footnote = format_illus_pack(c)
    return create_embed(c, m_title, m_description, m_footnote)


def format_player_card_deck(c, qty=0):
    name = c['name']
    level = format_xp(c)
    faction = faction_order[c['faction_code']] + format_faction(c)
    quantity = f"x{str(qty)}" if qty > 1 else ""
    subname = format_sub_text_short(c)

    text = f"{faction} {name}{subname} {level} {quantity}"
    return text


