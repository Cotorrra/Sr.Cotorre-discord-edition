from interactions import Option, OptionType, Choice

from src.api_interaction.cycle import cycle
from src.api_interaction.preview import preview
from src.core.translator import lang


def player_card_slash_options(name_req=False):
    """Returns the slash command options for player cards."""
    return [Option(name="name",
                   description=lang.locale('name_description'),
                   type=OptionType.STRING,
                   required=name_req),

            Option(name="level",
                   description=lang.locale('level_description'),
                   type=OptionType.NUMBER,
                   required=False),

            Option(name="faction",
                   description=lang.locale('faction_description'),
                   type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('guardian'), value="G"),
                       Choice(name=lang.locale('seeker'), value="B"),
                       Choice(name=lang.locale('rogue'), value="R"),
                       Choice(name=lang.locale('mystic'), value="M"),
                       Choice(name=lang.locale('survivor'), value="S"),
                       Choice(name=lang.locale('multiclass'), value="Mult"),
                       Choice(name=lang.locale('neutral'), value="N"),
                   ]),

            Option(name="extras",
                   description=lang.locale('extras_description'),
                   type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('permanent'), value="P"),
                       Choice(name=lang.locale('exceptional'), value="E"),
                       Choice(name=lang.locale('unique'), value="U"),
                       Choice(name=lang.locale('signature'), value="C"),
                   ]),

            Option(name="subtitle",
                   description=lang.locale('sub_description'),
                   type=OptionType.STRING,
                   required=False),

            Option(name="cycle",
                   description=lang.locale('pack_description'),
                   choices=[Choice(name=cy['name'], value=cy['sufix'])
                            for cy in cycle.get_cycle_data()],
                   type=OptionType.STRING,
                   required=False)
            ]


def deck_slash_options():
    """Returns the slash command options for decks"""
    return [Option(name="code",
                   description=lang.locale('deck_code_desc'),
                   type=OptionType.NUMBER,
                   required=True),

            Option(name="type",
                   description=lang.locale('deck_type_desc'),
                   type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('public_deck'), value="decklist"),
                       Choice(name=lang.locale('private_deck'), value="deck"),
                   ]),
            ]


def general_card_slash_options():
    """Returns the slash command options for general cards."""
    return [Option(name="name",
                   description=lang.locale('name_description'),
                   type=OptionType.STRING,
                   required=True),

            Option(name="type",
                   description=lang.locale('card_type_desc'),
                   type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('scenario'), value="S"),
                       Choice(name=lang.locale('act'), value="A"),
                       Choice(name=lang.locale('agenda'), value="P"),
                       Choice(name=lang.locale('treachery'), value="T"),
                       Choice(name=lang.locale('enemy'), value="E"),
                       Choice(name=lang.locale('location'), value="L"),
                       Choice(name=lang.locale('player_cards'), value="J"),
                   ]),

            Option(name="subtitle",
                   description=lang.locale('sub_description'),
                   type=OptionType.STRING,
                   required=False),

            Option(name="cycle",
                   description=lang.locale('pack_description'),
                   choices=[Choice(name=cy['name'], value=cy['sufix'])
                            for cy in cycle.get_cycle_data()],
                   type=OptionType.STRING,
                   required=False)
            ]


"""
def rules_slash_options():
    return [Option(name="rule",
                          description="Nombre de la regla/concepto.",
                          type=OptionType.STRING,
                          required=True)]
"""


def tarot_slash_options():
    """Returns the slash command options for Tarot cards."""
    return [Option(name="name",
                   description=lang.locale('name_description'),
                   type=OptionType.STRING,
                   required=False)]


def timing_slash_options():
    """Returns the slash command options for Game's Framework."""
    return [Option(name="timing",
                   description=lang.locale('timings_type_desc'),
                   type=OptionType.STRING,
                   required=True,
                   choices=[
                       Choice(name=lang.locale('mythos_phase'), value="M"),
                       Choice(name=lang.locale('investigation_phase'), value="I"),
                       Choice(name=lang.locale('enemy_phase'), value="E"),
                       Choice(name=lang.locale('upkeep_phase'), value="U"),
                       Choice(name=lang.locale('skill_test'), value="S"),
                   ])]


def preview_card_slash_options():
    """Returns the slash command options for previewed cards"""
    options = []
    preview_data = preview.get_preview_data()
    counter = 0
    while preview_data:
        preview_slice, preview_data = preview_data[:25], preview_data[25:]
        options.append(Option(
                name="card" + str(counter),
                description=lang.locale('name_description'),
                type=OptionType.STRING,
                required=False,
                choices=[Choice(name=c['name'], value=c['code']) for c in preview_slice]))
        counter += 1

    return options
