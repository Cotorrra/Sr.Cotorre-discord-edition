from discord_slash.utils.manage_commands import create_option, create_choice


def player_card_slash_options():
    """
    Returns the slash command options for player cards.
    :return:
    """
    return [create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
            create_option(name="nivel", description="Nivel de la carta", option_type=4, required=False),
            create_option(name="clase", description="Clase de la carta.", option_type=3, required=False,
                          choices=[
                              create_choice(name="Guardián", value="G"),
                              create_choice(name="Buscador", value="B"),
                              create_choice(name="Rebelde", value="R"),
                              create_choice(name="Místico", value="M"),
                              create_choice(name="Superviviente", value="S"),
                              create_choice(name="Neutral", value="N"),
                          ]),
            create_option(name="extras", description="Extras", option_type=3, required=False,
                          choices=[
                              create_choice(name="Permanente", value="P"),
                              create_choice(name="Excepcional", value="E"),
                              create_choice(name="Avanzada/Paralela", value="A"),
                              create_choice(name="Única", value="U"),
                              create_choice(name="Característica", value="C"),
                          ]),
            create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False),
            create_option(name="pack", description="Nombre del pack de la carta.", option_type=3, required=False)
            ]


def deck_slash_options():
    """
    Returns the slash command options for decks.
    :return:
    """
    return [create_option(name="codigo",
                          description="Código del mazo en ArkhamDB.",
                          option_type=4,
                          required=True),
            create_option(name="tipo", description="Tipo de Mazo", option_type=3, required=False,
                          choices=[
                              create_choice(name="Público", value="decklist"),
                              create_choice(name="Privado", value="deck"),
                          ]),
            ]


def general_card_slash_options():
    """
    Returns the slash command options for general cards.
    :return:
    """
    return [create_option(name="nombre", description="Nombre de la carta.", option_type=3, required=True),
            create_option(name="tipo", description="Tipo de la carta.", option_type=3, required=False,
                          choices=[
                              create_choice(name="Escenario", value="S"),
                              create_choice(name="Acto", value="A"),
                              create_choice(name="Plan", value="P"),
                              create_choice(name="Traición", value="T"),
                              create_choice(name="Enemigo", value="E"),
                              create_choice(name="Lugares", value="L"),
                              create_choice(name="Cartas de Jugador", value="J"),
                              create_choice(name="Mitos (Encuentros)", value="M"),
                          ]),
            create_option(name="subtitulo", description="Subtitulo de la carta.", option_type=3, required=False),
            create_option(name="pack", description="Nombre del pack de la carta.", option_type=3, required=False),
            ]


def rules_slash_options():
    """
    Returns the slash command options rules.
    :return:
    """
    return [create_option(name="regla",
                          description="Nombre de la regla/concepto.",
                          option_type=3,
                          required=True)]


def tarot_slash_options():
    """
    Returns the slash command options for Tarot cards.
    :return:
    """
    return [create_option(name="nombre",
                          description="Nombre de la carta, si no hay nombre se devuelve una al azar",
                          option_type=3,
                          required=False)]
