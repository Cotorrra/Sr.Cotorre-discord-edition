def split_files(src: str):
    splits = src.split("/")
    rest = ""
    for a in splits[:-1]:
        rest += f"{a}/"
    return rest


def is_lvl(card: dict, lvl: int):
    """
    Compares the level of a card with a number, if the card doesnt have a level it always returns false.
    :param card: card
    :param lvl: lvl
    :return:
    """
    if "xp" in card:
        return card["xp"] == lvl
    else:
        return False


def get_qty(deck, card_id):
    for c_id, qty in deck["slots"].items():
        if c_id == card_id:
            return qty
    return 0


def has_trait(card, trait):
    try:
        traits = card["real_traits"].lower().split()
        return f"{trait}." in traits

    except KeyError:
        return False


def text_if(template, text):
    if text:
        return template % text
    else:
        return ""


def get_code(card):
    card_id = card["code"]
    while card_id:
        try:
            return int(card_id)
        except ValueError:
            card_id = card_id[:-1]
    return 0
