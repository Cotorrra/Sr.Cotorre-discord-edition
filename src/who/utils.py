def transform_secondary_class(choice):
    """Transforms a choice into a multiple choice list.

    Arguments:
        choice -- The choice to be transformed.

    Returns:
        A list with the transformed choice.
    """
    new_choice = {}
    # Marion/Wendy||/???
    if choice["name"] == "Trait Choice":
        new_choice = []  # {"trait": ["blessed", "cursed"], "level": {"min": 0, "max": 5}}
        for option in choice["option_select"]:
            new_choice.append(option)

    # Charlie
    elif choice["name"] == "Class Choice":
        new_choice = [{"faction": choice["faction_select"], "level": choice["level"]}]

    # Carson/Mandy/Tony/Gloria/???
    elif choice["name"] == "Secondary Class":
        new_choice = [
            {
                "faction": choice["faction_select"],
                "level": choice["level"],
                "type": choice["type"],
            }
        ]

    return new_choice


def match_investigator_deck_options(inv, card):
    match_dict = {
        "faction": check_faction,
        "level": check_level,
        "trait": check_traits,
        "type": check_type,
        "tag": check_tag,
        "uses": check_uses,
        "text": check_text,
        "not": lambda x, y: True,
        "limit": lambda x, y: True,
        "error": lambda x, y: True,
        "atleast": lambda x, y: True,
        "id": lambda x, y: True,
        "name": lambda x, y: True,
        "permanent": lambda x, y: True,
        "base_level": lambda x, y: True,
    }
    for deck_option in inv["deck_options"]:
        check = True
        if "name" in deck_option:
            deck_option = transform_secondary_class(deck_option)
        else:
            deck_option = [deck_option]
        if deck_option:
            for option in deck_option:
                for key, value in option.items():
                    check = check and match_dict[key](card, value)
                if check:
                    if "not" in deck_option:
                        return not option["not"]
                    return True

    return False


def check_faction(card, f_list):
    faction1 = card["faction_code"]
    faction2 = card["faction2_code"] if "faction2_code" in card else ""
    faction3 = card["faction3_code"] if "faction3_code" in card else ""
    for faction in [faction1, faction2, faction3]:
        if faction in f_list:
            return True
    return False


def check_level(card, levels):
    return levels["min"] <= card["xp"] <= levels["max"]


def check_traits(card, traits):
    c_traits = card["real_traits"][:-1].lower()
    for t in traits:
        if t in c_traits:
            return True
    return False


def check_type(card, types):
    return card["type_code"] in types


def check_tag(card, tag):
    if "tags" in card:
        for t in tag:
            if t in card["tags"]:
                return True
    return False


def check_uses(card, uses):
    for use in uses:
        if use in card["real_text"] and "Uses" in card["real_text"]:
            return True
    return False


def check_text(card, text):
    for t in text:
        if t in card["real_text"]:
            return True
    return False


def filter_by_classes(investigators):
    return {
        "guardian": [inv for inv in investigators if inv["faction_code"] == "guardian"],
        "seeker": [inv for inv in investigators if inv["faction_code"] == "seeker"],
        "rogue": [inv for inv in investigators if inv["faction_code"] == "rogue"],
        "mystic": [inv for inv in investigators if inv["faction_code"] == "mystic"],
        "survivor": [inv for inv in investigators if inv["faction_code"] == "survivor"],
        "neutral": [inv for inv in investigators if inv["faction_code"] == "neutral"],
    }


def match_card_restrictions(investigator, card):
    """
    Given a Investigator and a card, it checks if the investigator can take the card +
    (considering card restrictions).
    """
    if "restrictions" not in card:
        return True

    for key, value in card["restrictions"].items():
        match key:
            case "trait":
                for trait in value:
                    if trait in investigator["real_traits"].lower():
                        return True

    return False
