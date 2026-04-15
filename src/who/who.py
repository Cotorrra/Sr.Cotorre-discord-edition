from src.api_interaction.taboo import taboo
from src.core.cards_db import cards
from src.core.formatting import create_embed, format_text
from src.core.translator import locale as _
from src.who.utils import (
    filter_by_classes,
    match_card_restrictions,
    match_investigator_deck_options,
)


def resolve_search_who(array):
    """Resolves the who command for a card."""
    if len(array) > 0:
        card = array[0]
        who_can_take = []
        who_cannot_take = []
        investigators = cards.get_investigators()
        if "xp" in card:
            for inv in investigators:
                card_restriction_result = match_card_restrictions(inv, card)
                deck_building_result = match_investigator_deck_options(inv, card)

                if card_restriction_result and deck_building_result:
                    who_can_take.append(inv)
                else:
                    who_cannot_take.append(inv)

            if 0 <= len(who_cannot_take) <= 10:
                embed = format_who(card, who_cannot_take, positive=False)
            else:
                embed = format_who(card, who_can_take)

            return embed
    return create_embed(_("ahWho_card_not_found"))


def format_who(card, array, positive=True):
    """Formats the who command for a card."""
    neg_text = "" if positive else "_neg"
    title = f"{_(f'ahWho_title{neg_text}')}: {card['name']}{taboo.format_xp(card)}"
    description = ""

    if len(array) == 0 and not positive:
        title = f"{_('ahWho_title')}: {card['name']}{taboo.format_xp(card)}"
        description = f"{_('ahWho_everyone')}"
        return create_embed(title=title, description=description, c=card)

    if not positive:
        description += f"{_('ahWho_neg_text')}"

    foot_note = ""
    if card["xp"] == 0 and card["faction_code"] != "neutral":
        foot_note = f"{format_text(_('ahWho_versatile_text'))}\n"

    embed = create_embed(
        title=title, description=description, c=card, footnote=foot_note
    )

    classes = filter_by_classes(array)

    for faction, investigators in classes.items():
        if investigators:
            class_inv = list(
                filter(
                    lambda x: x["faction_code"] == faction,
                    cards.get_investigators(),
                )
            )
            if len(class_inv) == len(investigators):
                description = f"{_('ahWho_all_class')}"
                title = f"{format_text('[' + faction + ']')}{_(faction)} ({len(investigators)}):"
                embed.add_field(name=title, value=description)
            else:
                names = [c["name"] for c in investigators]
                description = ", ".join(names)
                title = f"{format_text('[' + faction + ']')}{_(faction)} ({len(investigators)}):"
                embed.add_field(name=title, value=description)

    return embed
