from src.core.formating import format_name, format_subtext, format_faction, format_illus_pack, create_embed, \
    format_card_text, format_text
from src.faq.faq import load_faq, has_faq, get_faq
from src.p_cards.utils import format_xp


def format_faq(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "level": format_xp(c),
                "text": "> %s \n" % format_card_text(c) if "text" in c else "",
                "faq": format_faq_text(c['code'], back=False)
                }

    title = " %(faction)s%(name)s%(subtext)s%(level)s" % formater
    description = "%(text)s\n%(faq)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, title, description, m_footnote)


def format_faq_text(card_id, back=False):
    faq_info = load_faq(card_id)
    text = "**Preguntas frecuentes**: \n"
    if has_faq(card_id, faq_info):
        card = get_faq(card_id, faq_info)
        if back and ('text_back' in card):
            text += ">>> %s \n" % format_text(card['text_back'])
        elif 'text' in card:
            text += ">>> %s \n" % format_text(card['text'])
        return text
    else:
        return "Esta carta no tiene faq _(aún)_"