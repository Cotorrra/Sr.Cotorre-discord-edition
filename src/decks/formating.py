import discord
import werkzeug.datastructures

from config import ARKHAM_DB
from src.core.translator import lang
from src.p_cards.formating import format_player_card_deck


def format_assets(arr: [(dict, int)], key: str, taboo_info: str) -> str:
    text = ""
    if arr:
        text += f"_{lang.locale(key)}:_"
        aux = []
        for (c, q) in arr:
            aux.append(format_player_card_deck(c, q, taboo_info))
        aux = sorted(aux)
        for c in aux:
            text += "\n%s" % c[2:]
    return text


def format_all_assets(info: dict, taboo_info: str):
    types = ["assets", "assets_permanents"]
    text = ""
    for key in types:
        if info[key]:
            text += "%s\n" % format_assets(info[key], key, taboo_info)
    return text


def format_deck(deck, info):
    m_title = deck['name']

    investigator = f"{lang.locale('investigator')}: **{deck['investigator_name']}**"
    xp = f"_{lang.locale('xp_needed')}: {str(info['xp'])}_"
    m_description = f"{investigator}\n{xp}\n"

    deck_type = "decklist" if deck['user_id'] else "deck"
    url = f"{ARKHAM_DB}/{deck_type}/view/{deck['id']}"

    if info['assets_q'] > 0:
        assets = f"{lang.locale('assets')}: ({str(info['assets_q'])})"
        assets_cards = format_all_assets(info, info['taboo_id'])
        m_description += f"**{assets}**\n{assets_cards}\n"

    if info['events_q'] > 0:
        events = f"{lang.locale('events')}: ({str(info['events_q'])})"
        events_cards = format_list_of_cards(info['events'], info['taboo_id'])
        m_description += f"**{events}**\n{events_cards}\n"

    if info['skills_q'] > 0:
        skills = f"{lang.locale('skills')}: ({str(info['skills_q'])})"
        skills_cards = format_list_of_cards(info['skills'], info['taboo_id'])
        m_description += f"**{skills}**\n{skills_cards}\n"

    if info['treachery_q'] > 0:
        treachery = f"{lang.locale('treacheries/enemies')}: ({str(info['treachery_q'])})"
        treachery_cards = format_list_of_cards(info['treachery'], info['taboo_id'])
        m_description += f"**{treachery}**\n{treachery_cards}\n"

    embed = discord.Embed(title=m_title, description=m_description, color=info['color'], url=url)

    return embed


def format_upgraded_deck(deck1, info):
    m_title = deck1['name']

    investigator = f"{lang.locale('investigator')}: **{deck1['investigator_name']}**"
    xp = f"_{lang.locale('xp_needed')}: {str(info['xp_diff'])}_"
    m_description = f"{investigator}\n{xp}"

    url = f"{ARKHAM_DB}/deck/view/{deck1['id']}"
    embed = discord.Embed(title=m_title, description=m_description, color=info['color'], url=url)

    if len(info['buys_in']) > 0:
        embed.add_field(name=f"{lang.locale('added_cards')}:",
                        value=format_list_of_cards_upgr(info["buys_in"], info['taboo_id']), inline=True)

    if len(info['buys_out']) > 0:
        embed.add_field(name=f"{lang.locale('removed_cards')}:",
                        value=format_list_of_cards_upgr(info["buys_out"], info['taboo_id']), inline=True)

    return embed


def format_list_of_cards_upgr(arr, taboo_info):
    copy_arr = arr.copy()
    array = []

    while len(copy_arr) > 0:
        q = 0
        card = copy_arr[0]
        while card in copy_arr:
            q += 1
            copy_arr.remove(card)

        text = format_player_card_deck(card, q, taboo_info)
        array.append(text)
    array = sorted(array)
    text = ""
    for c in array:
        text += f"\n{c[2:]}\n"

    return text


def format_list_of_cards(arr, taboo_info="", sort=True):
    text = ""
    aux = []
    for (c, q) in arr:
        aux.append(format_player_card_deck(c, q, taboo_info))
    if sort:
        aux = sorted(aux)
    for c in aux:
        text += f"{c[2:]}\n"

    return text
