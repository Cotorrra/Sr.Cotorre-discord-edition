from interactions import OptionType, SlashCommandChoice, SlashCommandOption

from src.api_interaction.cycle import cycle
from src.api_interaction.preview import preview
from src.api_interaction.taboo import taboo
from src.core.cards_db import cards
from src.core.formatting import format_name
from src.core.translator import locale as _


def player_card_slash_options(name_req=False):
    """Returns the slash command options for player cards."""
    return [
        SlashCommandOption(
            name="name",
            description=_("name_description"),
            type=OptionType.STRING,
            required=name_req,
        ),
        SlashCommandOption(
            name="level",
            description=_("level_description"),
            type=OptionType.NUMBER,
            required=False,
        ),
        SlashCommandOption(
            name="faction",
            description=_("faction_description"),
            type=OptionType.STRING,
            required=False,
            choices=[
                SlashCommandChoice(name=_("guardian"), value="G"),
                SlashCommandChoice(name=_("seeker"), value="B"),
                SlashCommandChoice(name=_("rogue"), value="R"),
                SlashCommandChoice(name=_("mystic"), value="M"),
                SlashCommandChoice(name=_("survivor"), value="S"),
                SlashCommandChoice(name=_("multiclass"), value="Mult"),
                SlashCommandChoice(name=_("neutral"), value="N"),
            ],
        ),
        SlashCommandOption(
            name="extras",
            description=_("extras_description"),
            type=OptionType.STRING,
            required=False,
            choices=[
                SlashCommandChoice(name=_("permanent"), value="P"),
                SlashCommandChoice(name=_("exceptional"), value="E"),
                SlashCommandChoice(name=_("unique"), value="U"),
                SlashCommandChoice(name=_("signature"), value="C"),
            ],
        ),
        SlashCommandOption(
            name="subtitle",
            description=_("sub_description"),
            type=OptionType.STRING,
            required=False,
        ),
        SlashCommandOption(
            name="cycle",
            description=_("pack_description"),
            choices=[
                SlashCommandChoice(name=cy["name"], value=cy["sufix"])
                for cy in cycle.get_cycle_data()
            ],
            type=OptionType.STRING,
            required=False,
        ),
        SlashCommandOption(
            name="traits",
            description=_("traits_description"),
            type=OptionType.STRING,
            required=False,
        ),
    ]


def deck_slash_options():
    """Returns the slash command options for decks"""
    return [
        SlashCommandOption(
            name="code",
            description=_("deck_code_desc"),
            type=OptionType.NUMBER,
            required=True,
        ),
        SlashCommandOption(
            name="deck_type",
            description=_("deck_type_desc"),
            type=OptionType.STRING,
            required=False,
            choices=[
                SlashCommandChoice(name=_("public_deck"), value="decklist"),
                SlashCommandChoice(name=_("private_deck"), value="deck"),
            ],
        ),
    ]


def general_card_slash_options():
    """Returns the slash command options for general cards."""
    return [
        SlashCommandOption(
            name="name",
            description=_("name_description"),
            type=OptionType.STRING,
            required=True,
        ),
        SlashCommandOption(
            name="card_type",
            description=_("card_type_desc"),
            type=OptionType.STRING,
            required=False,
            choices=[
                SlashCommandChoice(name=_("scenario"), value="S"),
                SlashCommandChoice(name=_("act"), value="A"),
                SlashCommandChoice(name=_("agenda"), value="P"),
                SlashCommandChoice(name=_("treachery"), value="T"),
                SlashCommandChoice(name=_("enemy"), value="E"),
                SlashCommandChoice(name=_("location"), value="L"),
                SlashCommandChoice(name=_("player_cards"), value="J"),
            ],
        ),
        SlashCommandOption(
            name="subtitle",
            description=_("sub_description"),
            type=OptionType.STRING,
            required=False,
        ),
        SlashCommandOption(
            name="cycle",
            description=_("pack_description"),
            choices=[
                SlashCommandChoice(name=cy["name"], value=cy["sufix"])
                for cy in cycle.get_cycle_data()
            ],
            type=OptionType.STRING,
            required=False,
        ),
        SlashCommandOption(
            name="traits",
            description=_("traits_description"),
            type=OptionType.STRING,
            required=False,
        ),
    ]


def tarot_slash_options():
    """Returns the slash command options for Tarot cards."""
    return [
        SlashCommandOption(
            name="name",
            description=_("name_description"),
            type=OptionType.STRING,
            required=False,
        )
    ]


def timing_slash_options():
    """Returns the slash command options for Game's Framework."""
    return [
        SlashCommandOption(
            name="timing",
            description=_("timings_type_desc"),
            type=OptionType.STRING,
            required=True,
            choices=[
                SlashCommandChoice(name=_("mythos_phase"), value="M"),
                SlashCommandChoice(name=_("investigation_phase"), value="I"),
                SlashCommandChoice(name=_("enemy_phase"), value="E"),
                SlashCommandChoice(name=_("upkeep_phase"), value="U"),
                SlashCommandChoice(name=_("skill_test"), value="S"),
            ],
        )
    ]


def preview_card_slash_options():
    """Returns the slash command options for previewed cards"""
    options = []
    preview_data = preview.get_preview_data()
    counter = 0
    while preview_data:
        preview_slice, preview_data = preview_data[:25], preview_data[25:]
        options.append(
            SlashCommandOption(
                name="card" + str(counter),
                description=_("name_description"),
                type=OptionType.STRING,
                required=False,
                choices=[
                    SlashCommandChoice(
                        name=f"{format_name(c)}{taboo.format_xp(c)}", value=c["code"]
                    )
                    for c in preview_slice
                ],
            )
        )
        counter += 1
    return options


def customizable_card_slash_options():
    """Return the slash command options for costumizable upgrade cards"""
    customizable_cards = cards.get_customizable_cards()
    return [
        SlashCommandOption(
            name="name",
            description=_("name_description"),
            type=OptionType.STRING,
            required=True,
            choices=[
                SlashCommandChoice(name=f"{format_name(c)}", value=c["code"])
                for c in customizable_cards
            ],
        )
    ]
