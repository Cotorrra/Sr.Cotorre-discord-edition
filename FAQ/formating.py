from FAQ.faq import format_faq_text
from core.formating import format_name, format_subtext, format_faction, format_illus_pack, create_embed, \
    format_card_text
from p_cards.utils import format_xp


def format_faq(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "level": format_xp(c),
                "text": "> %s \n" % format_card_text(c, override_spoiler=True) if "text" in c else "",
                "FAQ": format_faq_text(c['code'], back=False)
                }

    title = " %(faction)s%(name)s%(subtext)s%(level)s" % formater
    description = "%(text)s\n%(FAQ)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, title, description, m_footnote)