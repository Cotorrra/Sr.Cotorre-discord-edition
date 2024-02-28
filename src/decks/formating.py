from interactions import Embed

from config import ARKHAM_DB
from src.api_interaction.taboo import taboo
from src.core.formating import faction_order, format_faction, format_text, slot_order
from src.core.translator import lang
from src.p_cards.utils import customize_card, extract_upgrades_names, format_slot, format_sub_text_short

def format_player_card_deck(card: dict, qty=0, taboo_info="", deck_meta={}) -> str:
    c = customize_card(card.copy(), deck_meta)
    name = c['name']
    level = taboo.format_xp(c, taboo_info, deck_meta)
    faction = format_faction(c)
    quantity = f"x{str(qty)}" if qty > 1 else ""
    subname = format_sub_text_short(c)
    slot = format_slot(c)
    priority_order = slot_order(c) + faction_order[c['faction_code']]
    taboo_text = format_text(" [taboo]") if taboo.is_in_taboo(c['code'], taboo_info) else ""
    text = f"{priority_order}{faction}{slot} {name}{subname} {level}{taboo_text} {quantity}"
    return text


def format_assets(arr: [(dict, int)], key: str, taboo_info: str, deck_meta: dict = {}) -> str:
    text = ""
    if arr:
        text += f"_{lang.locale(key)}:_"
        aux = []
        for (c, q) in arr:
            aux.append(format_player_card_deck(c, q, taboo_info, deck_meta))
        aux = sorted(aux)
        for c in aux:
            text += "\n%s" % c[2:]
    return text


def format_all_assets(info: dict, taboo_info: str, deck_meta: dict = {}) -> str:
    types = ["assets", "assets_permanents"]
    text = ""
    for key in types:
        if info[key]:
            text += "%s\n" % format_assets(info[key], key, taboo_info, deck_meta)
    return text


def format_deck(deck: dict, info: dict) -> Embed:
    m_title = deck['name']

    investigator = f"{lang.locale('investigator')}: **{deck['investigator_name']}**"
    xp = f"_{lang.locale('xp_needed')}: {str(info['xp'])}_"
    m_description = f"{investigator}\n{xp}\n"

    deck_type = "decklist" if deck['user_id'] else "deck"
    url = f"{ARKHAM_DB}/{deck_type}/view/{deck['id']}"

    if info['assets_q'] > 0:
        assets = f"{lang.locale('assets')}: ({str(info['assets_q'])})"
        assets_cards = format_all_assets(info, info['taboo_id'], deck_meta=info['deck_meta'])
        m_description += f"**{assets}**\n{assets_cards}\n"

    if info['events_q'] > 0:
        events = f"{lang.locale('events')}: ({str(info['events_q'])})"
        events_cards = format_list_of_cards(info['events'], info['taboo_id'], deck_meta=info['deck_meta'])
        m_description += f"**{events}**\n{events_cards}\n"

    if info['skills_q'] > 0:
        skills = f"{lang.locale('skills')}: ({str(info['skills_q'])})"
        skills_cards = format_list_of_cards(info['skills'], info['taboo_id'], deck_meta=info['deck_meta'])
        m_description += f"**{skills}**\n{skills_cards}\n"

    if info['treachery_q'] > 0:
        treachery = f"{lang.locale('treacheries/enemies')}: ({str(info['treachery_q'])})"
        treachery_cards = format_list_of_cards(info['treachery'], info['taboo_id'], deck_meta=info['deck_meta'])
        m_description += f"**{treachery}**\n{treachery_cards}\n"
    embed = Embed(title=m_title, description=m_description, color=info['color'], url=url)

    return embed


def format_upgraded_deck(deck1: dict, info: dict) -> Embed:
    m_title = deck1['name']

    investigator = f"{lang.locale('investigator')}: **{deck1['investigator_name']}**"
    xp = f"_{lang.locale('xp_upgrade')}: {str(info['xp_spent'])}/{str(info['xp_diff'])}_"
    m_description = f"{investigator}\n{xp}"

    url = f"{ARKHAM_DB}/deck/view/{deck1['id']}"
    embed = Embed(title=m_title, description=m_description, color=info['color'], url=url)

    if len(info['buys_in']) > 0:
        embed.add_field(name=f"{lang.locale('added_cards')}:",
                        value=format_list_of_cards_upgr(info["buys_in"], info['taboo_id']), inline=True)

    if len(info['buys_out']) > 0:
        embed.add_field(name=f"{lang.locale('removed_cards')}:",
                        value=format_list_of_cards_upgr(info["buys_out"], info['taboo_id']), inline=True)

    if len(info['cuz_upgrades_in']) > 0:
        embed.add_field(name=f"{lang.locale('upgraded_cuz_cards')}:",
                        value=format_cuz_upgrades(info['cuz_upgrades_in'], info['cuz_upgrades_cards'], info['taboo_id']), inline=True)
    return embed


def format_card_cuz_upg(card, upgrade, upgrade_name, taboo_info):
    name = card['name']
    faction = format_faction(card)
    priority_order = slot_order(card) + faction_order[card['faction_code']]
    taboo_text = format_text("[taboo]") if taboo.is_in_taboo(card['code'], taboo_info) else ""
    upgrade_info = f"(+{upgrade['xp']}pts"
    upgrade_info += f", {upgrade['info']})" if "info" in upgrade and card['code']!= "09080" else ")"
    upgrade_text = f"{priority_order}{faction} {name}{taboo_text}: {upgrade_name} {upgrade_info}"
    return upgrade_text


def format_cuz_upgrades(cards_upgrades, cards, taboo_info):
    array = []
    for card in cards:
        upgrades_names = extract_upgrades_names(card)
        for upgrade_id, upgrade_values in cards_upgrades[card['code']].items():
            upgrade_name = upgrades_names[int(upgrade_id)]
            upgrade_text = format_card_cuz_upg(card, upgrade_values, upgrade_name, taboo_info)
            array.append(upgrade_text)
    
    array = sorted(array)
    format_text = ""
    for c in array:
        format_text += f"{c[2:]}\n"

    return format_text

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


def format_list_of_cards(arr, taboo_info="", sort=True, deck_meta={}):
    text = ""
    aux = []
    for (c, q) in arr:
        aux.append(format_player_card_deck(c, q, taboo_info, deck_meta))
    if sort:
        aux = sorted(aux)
    for c in aux:
        text += f"{c[2:]}\n"

    return text
