from src.core.formating import format_name, format_subtext, format_faction, format_illus_pack, create_embed, \
    format_card_text, format_text
from src.core.translator import lang
from src.faq.faq import load_faq, has_faq, get_faq
from src.p_cards.utils import format_xp


def format_faq(c):
    name = format_name(c)
    subtext = format_subtext(c)
    faction = format_faction(c)
    level = format_xp(c)
    text = f"> {format_card_text(c)}"
    faq = format_faq_text(c['code'], back=False)

    title = f"{faction} {name}{subtext} {level}"
    description = f"{text}\n{faq}"
    m_footnote = format_illus_pack(c)
    return create_embed(c, title, description, m_footnote)


def format_faq_text(card_id, back=False):
    faq_info = load_faq()
    text = f"**{lang.locale('faq_title')}**: \n"
    if has_faq(card_id, faq_info):
        card = get_faq(card_id, faq_info)
        if back and ('text_back' in card):
            text += f">>> {format_text(card['text_back'])} \n"
        elif 'text' in card:
            text += f">>> {format_text(card['text'])} \n"
        return text
    else:
        return lang.locale('faq_not_found')
