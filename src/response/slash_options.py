from interactions import Option, OptionType, Choice
from src.api_interaction.cycle import cycle
from src.core.translator import lang


def player_card_slash_options(name_required=True):
    """
    Returns the slash command options for player cards.
    :return:
    """
    return [Option(name="name", description=lang.locale('name_description'), option_type=OptionType.STRING,
                   required=name_required),
            Option(name="level", description=lang.locale('level_description'), option_type=OptionType.NUMBER,
                   required=False),
            Option(name="class", description=lang.locale('faction_description'), option_type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('guardian'), value="Guardian"),
                       Choice(name=lang.locale('seeker'), value="Seeker"),
                       Choice(name=lang.locale('rogue'), value="Rogue"),
                       Choice(name=lang.locale('mystic'), value="Mystic"),
                       Choice(name=lang.locale('survivor'), value="Survivor"),
                       Choice(name=lang.locale('neutral'), value="Neutral"),
                       Choice(name=lang.locale('multiclass'), value="Multiclass"),
                   ]),
            Option(name="extras", description=lang.locale('extras_description'), option_type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('permanent'), value="Permanent"),
                       Choice(name=lang.locale('exceptional'), value="Exceptional"),
                       Choice(name=lang.locale('unique'), value="Unique"),
                       Choice(name=lang.locale('signature'), value="Signature"),
                   ]),
            Option(name="sub", description=lang.locale('sub_description'), option_type=OptionType.STRING,
                   required=False),
            Option(name="pack", description=lang.locale('pack_description'), option_type=OptionType.STRING,
                   required=False),
            Option(name="cycle", description=lang.locale('cycle_description'), option_type=OptionType.STRING,
                   required=False,
                   choices=[Choice(name=c['name'], value=c['sufix']) for c in cycle.get_cycle_data()]),
            Option(name="text", description=lang.locale('text_description'), option_type=OptionType.STRING,
                   required=False)
            ]


def deck_slash_options():
    """
    Returns the slash command options for decks.
    :return:
    """
    return [Option(name="code",
                   description=lang.locale('deck_code_desc'),
                   option_type=4,
                   required=True),
            Option(name="type", description=lang.locale('deck_type_desc'), option_type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('public_deck'), value="decklist"),
                       Choice(name=lang.locale('private_deck'), value="deck"),
                   ]),
            ]


def general_card_slash_options():
    """
    Returns the slash command options for general cards.
    :return:
    """
    return [
        Option(name="name", description=lang.locale('name_description'), option_type=OptionType.STRING, required=True),
        Option(name="type", description=lang.locale('card_type_desc'), option_type=OptionType.STRING, required=False,
               choices=[
                   Choice(name=lang.locale('scenario'), value="S"),
                   Choice(name=lang.locale('act'), value="A"),
                   Choice(name=lang.locale('agenda'), value="P"),
                   Choice(name=lang.locale('treachery'), value="T"),
                   Choice(name=lang.locale('enemy'), value="E"),
                   Choice(name=lang.locale('location'), value="L"),
                   Choice(name=lang.locale('player_cards'), value="J"),
                   Choice(name=lang.locale('mythos'), value="M"),
               ]),
        Option(name="sub", description=lang.locale('sub_description'), option_type=OptionType.STRING, required=False),
        Option(name="pack", description=lang.locale('pack_description'), option_type=OptionType.STRING, required=False),
        Option(name="cycle", description=lang.locale('cycle_description'), option_type=OptionType.STRING,
               required=False,
               choices=[Choice(name=c['name'], value=c['sufix']) for c in cycle.get_cycle_data()]),
        Option(name="text", description=lang.locale('text_description'), option_type=OptionType.STRING, required=False)
        ]


"""
def rules_slash_options():
    return [Option(name="rule",
                          description="Nombre de la regla/concepto.",
                          option_type=OptionType.STRING,
                          required=True)]
"""


def tarot_slash_options():
    """
    Returns the slash command options for Tarot cards.
    :return:
    """
    return [Option(name="name",
                   description=lang.locale('name_description'),
                   option_type=OptionType.STRING,
                   required=False)]


def timing_slash_options():
    """
    Returns the slash command options for Game's Framework.
    :return:
    """
    return [Option(name="timing",
                   description=lang.locale('timings_type_desc'),
                   option_type=OptionType.STRING,
                   required=True,
                   choices=[
                       Choice(name=lang.locale('mythos_phase'), value="M"),
                       Choice(name=lang.locale('investigation_phase'), value="I"),
                       Choice(name=lang.locale('enemy_phase'), value="E"),
                       Choice(name=lang.locale('upkeep_phase'), value="U"),
                       Choice(name=lang.locale('skill_test'), value="S"),
                   ])]


def random_slash_options():
    return player_card_slash_options(False) + \
           [Option(name="type", description=lang.locale('card_type_desc'), option_type=OptionType.STRING,
                   required=False,
                   choices=[
                       Choice(name=lang.locale('skills'), value="Skills"),
                       Choice(name=lang.locale('assets'), value="Asset"),
                       Choice(name=lang.locale('events'), value="Event"),
                       Choice(name=lang.locale('treachery'), value="Treachery"),
                       Choice(name=lang.locale('enemy'), value="Enemy"),
                   ]),
            Option(name="traits", description=lang.locale('trait_description'), option_type=OptionType.STRING,
                   required=False),
            Option(name="slot", description=lang.locale('text_description'), option_type=OptionType.STRING,
                   required=False),
            Option(name="spoiler", description=lang.locale('spoiler_description'), option_type=OptionType.STRING,
                   required=False),
            ]


def list_slash_options():
    return random_slash_options() + \
           [Option(name="sort_by", description=lang.locale('sort_by_description'), option_type=OptionType.STRING,
                   required=False)]
