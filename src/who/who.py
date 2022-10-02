from src.api_interaction.taboo import taboo
from src.core.cardsDB import cards
from src.core.formating import create_embed, format_text, color_picker
from src.core.translator import lang
from src.who.utils import match_investigator_deck_options, filter_by_classes


def resolve_search_who(array):
    if len(array) > 0:
        card = array[0]
        if 'xp' in card:
            investigators = cards.get_investigators()
            who_can_take = []
            who_cannot_take = []
            for inv in investigators:
                result = match_investigator_deck_options(inv, card)
                if result:
                    who_can_take.append(inv)
                else:
                    who_cannot_take.append(inv)

            if 0 <= len(who_cannot_take) <= 10:
                embed = format_who(card, who_cannot_take, positive=False)
            else:
                embed = format_who(card, who_can_take)

            return embed


def format_who(card, array, positive=True):
    neg_text = '' if positive else '_neg'
    title = f"{lang.locale(f'ahWho_title{neg_text}')}: {card['name']}{taboo.format_xp(card)}"
    description = ""

    if len(array) == 0 and not positive:
        title = f"{lang.locale(f'ahWho_title')}: {card['name']}{taboo.format_xp(card)}"
        description = f"{lang.locale('ahWho_everyone')}"
        return create_embed(title=title, description=description, c=card)

    if card['xp'] == 0 and card['faction_code'] != 'neutral':
        description += f"{format_text(lang.locale('ahWho_versatile_text'))}\n" \

    if not positive:
        description += f"{lang.locale('ahWho_neg_text')}"

    embed = create_embed(title=title, description=description, c=card)

    classes = filter_by_classes(array)

    for faction, investigators in classes.items():
        if investigators:
            names = [c['name'] for c in investigators]
            description = ", ".join(names)
            title = f"{format_text('[' + faction + ']')}{lang.locale(faction)} ({len(investigators)}):"
            embed.add_field(name=title,
                            value=description)

    return embed
