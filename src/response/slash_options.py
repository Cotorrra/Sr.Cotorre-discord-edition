from discord_slash.utils.manage_commands import create_option, create_choice

from src.core.translator import locale


def player_card_slash_options():
    """
    Returns the slash command options for player cards.
    :return:
    """
    return [create_option(name="name", description=locale('name_description'), option_type=3, required=True),
            create_option(name="level", description=locale('level_description'), option_type=4, required=False),
            create_option(name="faction", description=locale('faction_description'), option_type=3, required=False,
                          choices=[
                              create_choice(name=locale('guardian'), value="G"),
                              create_choice(name=locale('seeker'), value="B"),
                              create_choice(name=locale('rogue'), value="R"),
                              create_choice(name=locale('mystic'), value="M"),
                              create_choice(name=locale('survivor'), value="S"),
                              create_choice(name=locale('neutral'), value="N"),
                          ]),
            create_option(name="extras", description=locale('extras_description'), option_type=3, required=False,
                          choices=[
                              create_choice(name=locale('permanent'), value="P"),
                              create_choice(name=locale('exceptional'), value="E"),
                              create_choice(name=locale('advanced/parallel'), value="A"),
                              create_choice(name=locale('unique'), value="U"),
                              create_choice(name=locale('signature'), value="C"),
                          ]),
            create_option(name="sub", description=locale('sub_description'), option_type=3, required=False),
            create_option(name="pack", description=locale('pack_description'), option_type=3, required=False)
            ]


def deck_slash_options():
    """
    Returns the slash command options for decks.
    :return:
    """
    return [create_option(name="code",
                          description=locale('deck_code_desc'),
                          option_type=4,
                          required=True),
            create_option(name="type", description=locale('deck_type_desc'), option_type=3, required=False,
                          choices=[
                              create_choice(name=locale('public_deck'), value="decklist"),
                              create_choice(name=locale('private_deck'), value="deck"),
                          ]),
            ]


def general_card_slash_options():
    """
    Returns the slash command options for general cards.
    :return:
    """
    return [create_option(name="name", description=locale('name_description'), option_type=3, required=True),
            create_option(name="type", description=locale('card_type_desc'), option_type=3, required=False,
                          choices=[
                              create_choice(name=locale('scenario'), value="S"),
                              create_choice(name=locale('act'), value="A"),
                              create_choice(name=locale('agenda'), value="P"),
                              create_choice(name=locale('treachery'), value="T"),
                              create_choice(name=locale('enemy'), value="E"),
                              create_choice(name=locale('location'), value="L"),
                              create_choice(name=locale('player_cards'), value="J"),
                              create_choice(name=locale('mythos'), value="M"),
                          ]),
            create_option(name="sub", description=locale('sub_description'), option_type=3, required=False),
            create_option(name="pack", description=locale('pack_description'), option_type=3, required=False),
            ]


"""
def rules_slash_options():
    return [create_option(name="rule",
                          description="Nombre de la regla/concepto.",
                          option_type=3,
                          required=True)]
"""


def tarot_slash_options():
    """
    Returns the slash command options for Tarot cards.
    :return:
    """
    return [create_option(name="name",
                          description=locale('name_description'),
                          option_type=3,
                          required=False)]
