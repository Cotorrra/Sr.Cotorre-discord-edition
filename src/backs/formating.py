from src.core.formating import format_faction, format_name, format_subtext, format_card_text, format_set, \
    format_illus_pack, create_embed
from src.errata.formating import format_errata_text


def format_inv_card_b(c):
    formater = {"class": format_faction(c),
                "name": format_name(c),
                "subname": format_subtext(c),
                "deck_req": "> %s \n" % format_card_text(c, "back_text") if "back_text" in c else "",
                "flavour": "_%s_\n" % c['back_flavor'] if "back_flavor" in c else "",
                "errata_text": format_errata_text(c['code'], back=True),
                }
    m_title = "%(class)s %(name)s %(subname)s " % formater
    m_description = "%(deck_req)s \n" \
                    "%(flavour)s \n" \
                    "%(errata_text)s" % formater
    m_footnote = format_illus_pack(c)
    embed = create_embed(c, m_title, m_description, m_footnote)
    return embed


def format_location_card_b(c):
    formater = {"name": format_name(c),
                "back": "> %s \n" % format_card_text(c, "back_text") if "back_text" in c else "",
                "flavour": "_%s_\n" % format_card_text(c, "back_flavor") if "back_flavor" in c else "",
                }
    m_title = "%(name)s" % formater
    m_description = "%(back)s \n" \
                    "%(flavour)s" % formater
    m_footnote = format_illus_pack(c)
    embed = create_embed(c, m_title, m_description, m_footnote)
    return embed


def format_general_card_b(c):
    formater = {"name": format_name(c),
                "subname": format_subtext(c),
                "back": "> %s \n" % format_card_text(c, "back_text") if "back_text" in c else "",
                "pack": format_set(c),
                "flavour": "_%s_\n" % c['back_flavor'] if "back_flavor" in c else "",
                }
    m_title = "%(name)s %(subname)s" % formater
    m_description = "%(back)s \n" \
                    "%(flavour)s" % formater
    m_footnote = "%(pack)s" % formater
    embed = create_embed(c, m_title, m_description, m_footnote)
    return embed
