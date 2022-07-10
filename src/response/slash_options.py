from discord_slash.utils.manage_commands import create_option, create_choice

from src.core.translator import lang


def player_card_slash_options():
    """Returns the slash command options for player cards."""
    return [create_option(name="name",
                          description=lang.locale('name_description'),
                          option_type=3,
                          required=False),

            create_option(name="level",
                          description=lang.locale('level_description'),
                          option_type=4,
                          required=False),

            create_option(name="faction",
                          description=lang.locale('faction_description'),
                          option_type=3,
                          required=False,
                          choices=[
                              create_choice(name=lang.locale('guardian'), value="G"),
                              create_choice(name=lang.locale('seeker'), value="B"),
                              create_choice(name=lang.locale('rogue'), value="R"),
                              create_choice(name=lang.locale('mystic'), value="M"),
                              create_choice(name=lang.locale('survivor'), value="S"),
                              create_choice(name=lang.locale('multiclass'), value="Mult"),
                              create_choice(name=lang.locale('neutral'), value="N"),
                          ]),

            create_option(name="extras",
                          description=lang.locale('extras_description'),
                          option_type=3,
                          required=False,
                          choices=[
                              create_choice(name=lang.locale('permanent'), value="P"),
                              create_choice(name=lang.locale('exceptional'), value="E"),
                              create_choice(name=lang.locale('advanced/parallel'), value="A"),
                              create_choice(name=lang.locale('unique'), value="U"),
                              create_choice(name=lang.locale('signature'), value="C"),
                          ]),

            create_option(name="sub",
                          description=lang.locale('sub_description'),
                          option_type=3,
                          required=False),

            create_option(name="pack",
                          description=lang.locale('pack_description'),
                          option_type=3,
                          required=False)
            ]


def deck_slash_options():
    """Returns the slash command options for decks"""
    return [create_option(name="code",
                          description=lang.locale('deck_code_desc'),
                          option_type=4,
                          required=True),

            create_option(name="type",
                          description=lang.locale('deck_type_desc'),
                          option_type=3,
                          required=False,
                          choices=[
                              create_choice(name=lang.locale('public_deck'), value="decklist"),
                              create_choice(name=lang.locale('private_deck'), value="deck"),
                          ]),
            ]


def general_card_slash_options():
    """Returns the slash command options for general cards."""
    return [create_option(name="name",
                          description=lang.locale('name_description'),
                          option_type=3,
                          required=False),

            create_option(name="type",
                          description=lang.locale('card_type_desc'),
                          option_type=3,
                          required=False,
                          choices=[
                              create_choice(name=lang.locale('scenario'), value="S"),
                              create_choice(name=lang.locale('act'), value="A"),
                              create_choice(name=lang.locale('agenda'), value="P"),
                              create_choice(name=lang.locale('treachery'), value="T"),
                              create_choice(name=lang.locale('enemy'), value="E"),
                              create_choice(name=lang.locale('location'), value="L"),
                              create_choice(name=lang.locale('player_cards'), value="J"),
                              create_choice(name=lang.locale('mythos'), value="M"),
                          ]),

            create_option(name="sub",
                          description=lang.locale('sub_description'),
                          option_type=3,
                          required=False),

            create_option(name="pack",
                          description=lang.locale('pack_description'),
                          option_type=3,
                          required=False),
            ]


"""
def rules_slash_options():
    return [create_option(name="rule",
                          description="Nombre de la regla/concepto.",
                          option_type=3,
                          required=True)]
"""


def tarot_slash_options():
    """Returns the slash command options for Tarot cards."""
    return [create_option(name="name",
                          description=lang.locale('name_description'),
                          option_type=3,
                          required=False)]


def timing_slash_options():
    """Returns the slash command options for Game's Framework."""
    return [create_option(name="timing",
                          description=lang.locale('timings_type_desc'),
                          option_type=3,
                          required=True,
                          choices=[
                              create_choice(name=lang.locale('mythos_phase'), value="M"),
                              create_choice(name=lang.locale('investigation_phase'), value="I"),
                              create_choice(name=lang.locale('enemy_phase'), value="E"),
                              create_choice(name=lang.locale('upkeep_phase'), value="U"),
                              create_choice(name=lang.locale('skill_test'), value="S"),
                          ])]
