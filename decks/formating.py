import discord

from p_cards.formating import format_player_card_deck


def format_assets(arr, title):
    text = ""
    if arr:
        text += "_%s:_" % title
        aux = []
        for (c, q) in arr:
            aux.append(format_player_card_deck(c, q))
        aux = sorted(aux)
        for c in aux:
            text += "\n%s" % c[1:]
    return text


def format_all_assets(info):
    types = {"assets_h": "Mano", "assets_h2": "Mano x2", "assets_b": "Cuerpo",
             "assets_acc": "Accesorio", "assets_ar": "Arcano", "assets_ar2": "Arcano x2", "assets_ally": "Aliado",
             "assets_o": "Otros", "permanents": "Permanentes"}
    text = ""
    for key, value in types.items():
        if info[key]:
            text += "%s\n" % format_assets(info[key], value)
    return text


def format_deck(deck, info):
    formater = {"name": "%s" % deck['name'],
                "investigator": "_Mazo para %s_" % deck['investigator_name'],
                "xp": "Experiencia Necesaria: %s" % str(info['xp']),
                "assets": "Apoyos: (%s)" % str(info["assets_q"]) if info['assets_q'] > 0 else "",
                "events": "Eventos: (%s)" % str(info["events_q"]) if info['events_q'] > 0 else "",
                "skills": "Habilidades: (%s)" % str(info["skills_q"]) if info['skills_q'] > 0 else "",
                "treachery": "Traiciones/Enemigos: (%s)" % str(info["treachery_q"]) if info['treachery_q'] > 0 else "",
                }

    m_title = "%(name)s" % formater
    m_description = "%(investigator)s \n" \
                    "%(xp)s" % formater

    inline = False
    if deck['user_id']:
        url = "https://es.arkhamdb.com/decklist/view/%s" % deck['id']
    else:
        url = "https://es.arkhamdb.com/deck/view/%s" % deck['id']
    embed = discord.Embed(title=m_title, description=m_description, color=info['color'], url=url)
    if info['assets_q'] > 0:
        embed.add_field(name="%(assets)s" % formater, value=format_all_assets(info), inline=inline)

    if info['events_q'] > 0:
        embed.add_field(name="%(events)s" % formater, value=format_list_of_cards(info['events']), inline=inline)

    if info['skills_q'] > 0:
        embed.add_field(name="%(skills)s" % formater, value=format_list_of_cards(info['skills']), inline=inline)

    if info['treachery_q'] > 0:
        embed.add_field(name="%(treachery)s" % formater, value=format_list_of_cards(info['treachery']), inline=inline)

    return embed


def format_upgraded_deck(deck1, info):
    formater = {"name": "%s" % deck1['name'],
                "investigator": "_Mazo para %s_" % deck1['investigator_name'],
                "xp": "Experiencia Utilizada: %s" % str(info['xp_diff']),
                }

    m_title = "%(name)s" % formater
    m_description = "%(investigator)s \n" \
                    "%(xp)s" % formater

    url = "https://es.arkhamdb.com/deck/view/%s" % deck1['id']
    embed = discord.Embed(title=m_title, description=m_description, color=info['color'], url=url)

    if len(info['buys_in']) > 0:
        embed.add_field(name="Cartas añadidas:",
                        value=format_list_of_cards_upgr(info["buys_in"]), inline=True)

    if len(info['buys_out']) > 0:
        embed.add_field(name="Cambios retiradas:",
                        value=format_list_of_cards_upgr(info["buys_out"]), inline=True)

    return embed


def format_list_of_cards_upgr(arr):
    copy_arr = arr.copy()
    array = []

    while len(copy_arr) > 0:
        q = 0
        card = copy_arr[0]
        while card in copy_arr:
            q += 1
            copy_arr.remove(card)

        text = format_player_card_deck(card, q)
        array.append(text)
    array = sorted(array)
    text = ""
    for c in array:
        text += "\n%s" % c[1:]

    return text


def format_list_of_cards(arr):
    text = ""
    aux = []
    for (c, q) in arr:
        aux.append(format_player_card_deck(c, q))
    aux = sorted(aux)
    for c in aux:
        text += "\n%s" % c[1:]

    return text
