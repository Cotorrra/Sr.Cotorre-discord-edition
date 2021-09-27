import discord

from config import arkhamdb
from src.core.translator import locale
from src.p_cards.formating import format_player_card_deck


def format_assets(arr: [(dict, int)], key: str) -> str:
    text = ""
    if arr:
        text += f"_{locale(key)}:_"
        aux = []
        for (c, q) in arr:
            aux.append(format_player_card_deck(c, q))
        aux = sorted(aux)
        for c in aux:
            text += "\n%s" % c[1:]
    return text


def format_all_assets(info: dict):
    types = ["assets_hand", "assets_hand2", "assets_body",
             "assets_accessory", "assets_arcane", "assets_arcane2", "assets_ally",
             "assets_others", "assets_permanents"]
    text = ""
    for key in types:
        if info[key]:
            text += "%s\n" % format_assets(info[key], key)
    return text


def format_deck(deck, info):
    m_title = deck['name']

    investigator = f"{locale('investigator')}: **{deck['investigator_name']}**"
    xp = f"_{locale('xp_needed')}: {str(info['xp'])}_"
    m_description = f"{investigator}\n{xp}"

    deck_type = "decklist" if deck['user_id'] else "deck"
    url = f"{arkhamdb}/{deck_type}/view/{deck['id']}"

    embed = discord.Embed(title=m_title, description=m_description, color=info['color'], url=url)

    # Keep it false, it looks ugly with its activated.
    inline = False
    if info['assets_q'] > 0:
        assets = f"{locale('assets')}: ({str(info['assets_q'])})"
        embed.add_field(name=assets, value=format_all_assets(info), inline=inline)

    if info['events_q'] > 0:
        events = f"{locale('events')}: ({str(info['events_q'])})"
        embed.add_field(name=events, value=format_list_of_cards(info['events']), inline=inline)

    if info['skills_q'] > 0:
        skills = f"{locale('skills')}: ({str(info['skills_q'])})"
        embed.add_field(name=skills, value=format_list_of_cards(info['skills']), inline=inline)

    if info['treachery_q'] > 0:
        treachery = f"{locale('treacheries/enemies')}: ({str(info['treachery_q'])})"
        embed.add_field(name=treachery, value=format_list_of_cards(info['treachery']), inline=inline)

    return embed


def format_upgraded_deck(deck1, info):
    m_title = deck1['name']

    investigator = f"{locale('investigator')}: **{deck1['investigator_name']}**"
    xp = f"_{locale('xp_needed')}: {str(info['xp_diff'])}_"
    m_description = f"{investigator}\n{xp}"

    url = f"{arkhamdb}/deck/view/{deck1['id']}"
    embed = discord.Embed(title=m_title, description=m_description, color=info['color'], url=url)

    if len(info['buys_in']) > 0:
        embed.add_field(name=f"{locale('added_cards')}:",
                        value=format_list_of_cards_upgr(info["buys_in"]), inline=True)

    if len(info['buys_out']) > 0:
        embed.add_field(name=f"{locale('removed_cards')}:",
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
        text += f"\n{c[1:]}"

    return text


def format_list_of_cards(arr):
    text = ""
    aux = []
    for (c, q) in arr:
        aux.append(format_player_card_deck(c, q))
    aux = sorted(aux)
    for c in aux:
        text += f"\n{c[1:]}"

    return text
