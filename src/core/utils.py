import json
import os

import requests


def load_from_repo(file_src):
    try:
        with open(file_src, "r", encoding='utf-8') as pack:
            info = json.load(pack)
    except FileNotFoundError as e:
        # Get the file from and download it to
        url = f"https://raw.githubusercontent.com/Cotorrra/Sr.Cotorre-Data/main/{file_src}"
        req = requests.get(url)
        path = split_files(file_src)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(file_src, 'w', encoding='utf-8') as pack:
            pack.write(req.text)

        info = json.loads(req.text)

    return info


def split_files(src: str):
    splits = src.split("/")
    rest = ""
    for a in splits[:-1]:
        rest += f"{a}/"
    return rest


def is_lvl(card: dict, lvl: int):
    """
    Compares the level of a card with a number, if the card doesnt have a level it always returns false.
    :param card: carta
    :param lvl: nivel
    :return:
    """
    if 'xp' in card:
        return card['xp'] == lvl
    else:
        return False


def get_qty(deck, card_id):
    for c_id, qty in deck['slots'].items():
        if c_id == card_id:
            return qty
    return 0


def has_trait(card, trait):
    try:
        traits = card['real_traits'].lower().split()
        return "%s." % trait in traits

    except KeyError:
        return False


def text_if(template, text):
    if text:
        return template % text
    else:
        return ""
