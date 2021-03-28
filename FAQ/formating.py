from FAQ.faq import format_faq_text
from core.formating import format_name, format_subtext, format_faction, format_illus_pack, create_embed, \
    format_card_text
from e_cards.formating import format_enemy_card_short, format_treachery_card_short, format_act_card_f_short, \
    format_agenda_card_f_short, format_scenario_card_short, format_location_card_f_short
from p_cards.formating import format_inv_card_f_short, format_player_card_short
from p_cards.utils import format_xp


def format_faq(c):
    formater = {"name": format_name(c),
                "subtext": format_subtext(c),
                "faction": format_faction(c),
                "level": format_xp(c),
                "text": "> %s \n" % format_card_text(c, override_spoiler=True) if "text" in c else "",
                "FAQ": format_faq_text(c['code'], back=False)
                }
    if c['type_code'] == "investigator":
        description = format_inv_card_f_short(c)

    elif c['type_code'] == "enemy":
        description = format_enemy_card_short(c)

    elif c['type_code'] == "treachery":
        description = format_treachery_card_short(c)

    elif c['type_code'] == 'act':
        description = format_act_card_f_short(c)

    elif c['type_code'] == 'agenda':
        description = format_agenda_card_f_short(c)

    elif c['type_code'] == 'location':
        description = format_location_card_f_short(c)

    elif c['type_code'] == 'scenario':
        description = format_scenario_card_short(c)
    else:
        description = format_player_card_short(c)

    title = " %(faction)s%(name)s%(subtext)s%(level)s" % formater
    description += "\n\n%(text)s\n%(FAQ)s" % formater
    m_footnote = format_illus_pack(c)
    return create_embed(c, title, description, m_footnote)