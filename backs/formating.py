import discord.embeds

from core.formating import format_faction, format_name, format_subtext, format_card_text, format_illustrator, \
    format_set, color_picker, set_thumbnail_image, format_illus_pack
from errata.errata import format_errata_text


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
    url = "https://es.arkhamdb.com/card/%s" % c['code']
    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c), url=url)
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed, True)
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

    url = "https://es.arkhamdb.com/card/%s" % c['code']
    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c), url=url)
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed, True)
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

    url = "https://es.arkhamdb.com/card/%s" % c['code']
    embed = discord.Embed(title=m_title, description=m_description, color=color_picker(c), url=url)
    embed.set_footer(text=m_footnote)
    set_thumbnail_image(c, embed, True)
    return embed
