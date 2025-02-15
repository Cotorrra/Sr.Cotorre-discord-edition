from interactions import Embed

from src.core.formatting import (
    format_faction,
    format_name,
    format_subtext,
    format_card_text,
    format_set,
    format_illus_pack,
    create_embed,
)
from src.core.utils import text_if
from src.api_interaction.errata import errata


def format_inv_card_b(c: dict) -> Embed:
    """Format an investigator card's back side."""
    faction = format_faction(c)
    name = format_name(c)
    subname = format_subtext(c)
    deck_req = text_if("> %s", format_card_text(c, "back_text"))
    flavour = f"_{format_card_text(c, 'back_flavor')}_"
    errata_text = errata.format_errata_text(c["code"], back=True)

    m_title = f"{faction} {name} {subname}"
    m_description = f"{deck_req}\n\n{flavour}\n\n{errata_text}"
    m_footnote = format_illus_pack(c)
    embed = create_embed(m_title, m_description, c, m_footnote)
    return embed


def format_location_card_b(c: dict) -> Embed:
    """Format a location card's back side."""
    name = format_name(c)
    back = text_if("> %s", format_card_text(c, "back_text"))
    flavour = f"_{format_card_text(c, 'back_flavor')}_"

    m_title = name
    m_description = f"{back}\n\n{flavour}"
    m_footnote = format_illus_pack(c)
    embed = create_embed(m_title, m_description, c, m_footnote)
    return embed


def format_general_card_b(c: dict) -> Embed:
    """Format a general card's back side."""
    name = format_name(c)
    subname = format_subtext(c)
    back = text_if("> %s", format_card_text(c, "back_text"))
    pack = format_set(c)
    flavour = f"_{format_card_text(c, 'back_flavor')}_"

    m_title = f"{name} {subname}"
    m_description = f"{flavour}\n\n{back}"
    m_footnote = pack
    embed = create_embed(m_title, m_description, c, m_footnote)
    return embed
