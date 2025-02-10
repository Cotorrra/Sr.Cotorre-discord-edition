from interactions import Embed

from config import ARKHAM_DB
from src.core.translator import locale as _
from src.p_cards.formatting import format_player_card_deck


def format_assets(arr, key: str, taboo_info: str) -> str:
    text = ""
    if arr:
        text += f"_{_(key)}:_"
        aux = []
        for c, q in arr:
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
    m_title = deck["name"]

    investigator = f"{_('investigator')}: **{deck['investigator_name']}**"
    xp = f"_{_('xp_needed')}: {str(info['xp'])}_"
    m_description = f"{investigator}\n{xp}\n"

    deck_type = "decklist" if deck["user_id"] else "deck"
    url = f"{ARKHAM_DB}/{deck_type}/view/{deck['id']}"

    if info["assets_q"] > 0:
        assets = f"{_('assets')}: ({str(info['assets_q'])})"
        assets_cards = format_all_assets(info, info["taboo_id"])
        m_description += f"**{assets}**\n{assets_cards}\n"

    if info["events_q"] > 0:
        events = f"{_('events')}: ({str(info['events_q'])})"
        events_cards = format_list_of_cards(info["events"], info["taboo_id"])
        m_description += f"**{events}**\n{events_cards}\n"

    if info["skills_q"] > 0:
        skills = f"{_('skills')}: ({str(info['skills_q'])})"
        skills_cards = format_list_of_cards(info["skills"], info["taboo_id"])
        m_description += f"**{skills}**\n{skills_cards}\n"

    if info["treachery_q"] > 0:
        treachery = f"{_('treacheries/enemies')}: ({str(info['treachery_q'])})"
        treachery_cards = format_list_of_cards(info["treachery"], info["taboo_id"])
        m_description += f"**{treachery}**\n{treachery_cards}\n"
    embed = Embed(
        title=m_title, description=m_description, color=info["color"], url=url
    )

    return embed


def format_upgraded_deck(deck1, info):
    m_title = deck1["name"]

    investigator = f"{_('investigator')}: **{deck1['investigator_name']}**"
    xp = f"_{_('xp_upgrade')}: {str(info['xp_spent'])}/{str(info['xp_diff'])}_"
    m_description = f"{investigator}\n{xp}"

    url = f"{ARKHAM_DB}/deck/view/{deck1['id']}"
    embed = Embed(
        title=m_title, description=m_description, color=info["color"], url=url
    )

    if len(info["buys_in"]) > 0:
        embed.add_field(
            name=f"{_('added_cards')}:",
            value=format_list_of_cards_upgr(info["buys_in"], info["taboo_id"]),
            inline=True,
        )

    if len(info["buys_out"]) > 0:
        embed.add_field(
            name=f"{_('removed_cards')}:",
            value=format_list_of_cards_upgr(info["buys_out"], info["taboo_id"]),
            inline=True,
        )

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
        text += f"{c[2:]}\n"
    return text


def format_list_of_cards(arr, taboo_info="", sort=True):
    text = ""
    aux = []
    for c, q in arr:
        aux.append(format_player_card_deck(c, q, taboo_info))
    if sort:
        aux = sorted(aux)
    for c in aux:
        text += f"{c[2:]}\n"

    return text
