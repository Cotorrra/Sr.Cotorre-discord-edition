import re

import requests
import unidecode

from config import ARKHAM_DB

pack_data = requests.get(f'{ARKHAM_DB}/api/public/packs/').json()


def card_search(query, cards, keyword_func):
    """
    Search a card within a set of cards using keywords (ex (4E))

    :param query: The card query.
    :param cards: Set of cards
    :param keyword_func: A keyword function
    :return:
    """
    query, keyword_query, keyword_mode = find_and_extract(query, "(", ")")
    query, sub_query, sub_text_mode = find_and_extract(query, "~", "~")
    query, pack_query, pack_mode = find_and_extract(query, "[", "]")
    f_cards = cards.copy()

    if sub_text_mode:
        f_cards = [c for c in f_cards if filter_by_subtext(c, sub_query)]
        f_cards = sorted(f_cards, key=lambda card: -hits_in_string(card['subname'], sub_query))

    if keyword_mode:
        f_cards = keyword_func(f_cards, keyword_query)

    if pack_mode:
        pack_search = sorted([pd['name'] for pd in pack_data], key=lambda pd: -hits_in_string(pack_query, pd))
        if len(pack_search) > 0:
            pack_tag = [pd["code"] for pd in pack_data if pd["name"].lower() == pack_search[0].lower()][0]
            f_cards = [c for c in f_cards if c["pack_code"] == pack_tag]

    cards_were_filtered = len(cards) > len(f_cards)

    r_cards = card_filter(query, f_cards)

    if len(r_cards) == 0 \
            or (not cards_were_filtered and len(r_cards) == len(f_cards)) \
            or (cards_were_filtered and len(r_cards) == len(cards)):
        return []
    else:
        return r_cards


def card_filter(query: str, cards: [dict]):
    """
    Filters the cards withing the group of cards that were given

    :param query: The query text
    :param cards: A list of cards
    :return:
    """
    r_cards = sorted(cards, key=lambda card: -hits_in_string(query, card['name'] + " " + card['real_name']))
    r_cards = [c for c in r_cards if hits_in_string(query, c['name'] + " " + c['real_name']) > 0]
    return r_cards


def find_by_id(code: str, cards: [dict]):
    """
    Returns the card with the given code. If it doesnt exits it returns false.
    :param code: The card code (i.e 10001)
    :param cards: The list of cards
    :return:
    """
    r_cards = [c for c in cards if c['code'] == code]
    try:
        return r_cards[0]
    except IndexError:
        return False


def filter_by_subtext(card: dict, sub: str):
    """
    Returns whether a card contains the given subname or not.

    :param card: a card
    :param sub: a subname
    :return:
    """
    if "subname" in card:
        return hits_in_string(card['subname'], sub) > 0
    else:
        return False


def find_and_extract(string: str, start_s: str, end_s: str):
    """
    Finds and extracts a substring delimited by start_s and end_s, returning two values:
    - The base string with that substring extracted
    - The substring that was extracted
    - Whether something was extracted or not.

    :param string:
    :param start_s:
    :param end_s:
    :return:
    """
    if start_s == end_s:
        enable = string.find(start_s) > 0
    else:
        enable = string.__contains__(start_s) and string.__contains__(end_s)

    if enable:
        fst_occ = string.find(start_s) + 1
        snd_occ = string[fst_occ:].find(end_s)
        extract = string[fst_occ: fst_occ + snd_occ]
        base = string.replace(" %s%s%s" % (start_s, extract, end_s), "", 1)
        return base, extract, enable
    else:
        return string, "", enable


def hits_in_string(query: str, find: str):
    """
    Returns the "hits" of the query string in the find string.

    Va por palabras.
    :param find:
    :param query:
    :return:
    """
    hits = 0
    set1 = query.lower().replace("-", " ").split()
    set2 = find.lower().replace("-", " ").split()
    hit_list = []
    for w1 in set1:
        for w2 in set2:
            w1_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w1))
            w2_c = re.sub(r'[^a-z0-9]', '', unidecode.unidecode(w2))
            if w1_c == w2_c and w1_c not in hit_list:
                hits += len(w1_c)
                hit_list.append(w1_c)
    return hits
