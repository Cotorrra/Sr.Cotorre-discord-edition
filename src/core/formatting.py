from interactions import Embed

from config import ARKHAM_DB, TEXT_FORMAT
from src.api_interaction.cycle import cycle
from src.core.translator import locale as _
from src.core.utils import get_code


def create_embed(title: str, description="", c=None, footnote="") -> Embed:
    """
    Creates a Discord embed with a title, description and footnote of a card.

    :param c: Card information dict.
    :param title: Card title
    :param description: Card description.
    :param footnote: Card footnote (optional)
    :return: A Discord embed.
    """
    if c:
        url = f"{ARKHAM_DB}/card/{c['code']}"
        embed = Embed(
            title=title, description=description, color=color_picker(c), url=url
        )
        set_thumbnail_image(c, embed)
    else:
        embed = Embed(title=title, description=description, color=0xAAAAAA)
    if footnote:
        embed.set_footer(footnote)
    return embed


def format_text(text: str) -> str:
    """
    Replaces certain text tags in a text to its matching emojis in Discord.

    :param text: The text
    :return: A new formatted text
    """
    for key, value in TEXT_FORMAT.items():
        text = text.replace(key, value)

    return text


def format_set(c: dict) -> str:
    """
    Returns the encounter set and pack of a given card.
    Ex: Rats are: Core Set #159. Rats #1-3.
    If the product comes from a Blister of a Cycle:
    ex:

    :param c: Card information.
    :return: String with text info.
    """
    pack_name = ""
    if 2000 < get_code(c) < 8000:
        pack_name = cycle.get_cycle_name(c["code"])
    else:
        pack_name = c["pack_name"]

    if "pack_name" in c and "position" in c:
        text = f"{pack_name} #{str(c['position'])}"
        if "encounter_code" in c:
            text += f": {c['encounter_name']} #{str(c['encounter_position'])}"
            if c["quantity"] > 1:
                text += f"-{str(c['encounter_position'] + c['quantity'] - 1)}"
        return text
    return _("preview_set")


def format_card_text(c: dict, tag="text") -> str:
    """
    Formats tagged text from a tag in a Card.

    :param c: Card information.
    :param tag: The tag to get the text.
    :return: A formatted text.
    """
    formatting = {"\n": "\n> "}
    if tag in c:
        text = format_text(c[tag])
    else:
        return ""

    for key, value in formatting.items():
        text = text.replace(key, value)
    return text


def format_illus_pack(c: dict, only_pack=False) -> str:
    """
    Formats the illustrator and pack of a card.
    Ex:
    Scavenging is:
        🖌 Derk Venneman
        Core Set #73.

    :param c:
    :param only_pack:
    :return:
    """
    pack = format_set(c)
    illustrator = format_illustrator(c)
    if only_pack:
        return f"{pack}"
    else:
        return f"{illustrator}\n{pack}"


def format_victory(c: dict) -> str:
    """
    Formats the victory points from a card.

    :param c: The card info.
    :return: A string
    """

    if "victory" in c:
        return f"**{_('victory')} {c['victory']}.**"
    else:
        return ""


def format_vengeance(c: dict) -> str:
    """
    Formats the evil vengeance (Yig) points from a card.

    :param c: The card info.
    :return: A string.
    """
    if "vengeance" in c:
        return f"**{_('vengeance')} {c['vengeance']}.**"
    else:
        return ""


def format_number(n) -> str:
    """
    Formats a number, yes. Some numbers need some formatting.
    The only rule for now is that if the number is -2 then the number it's X.

    :param n: A number
    :return: A string
    """
    if int(n) == -2:
        return "X"
    else:
        return str(n)


def format_faction(c: dict) -> str:
    """
    Formats the different classes that could be in a card.
    Thanks EotE.

    :param c: A card info.
    :return: A string
    """
    if "faction3_code" in c:
        return format_text(
            f"[{c['faction_code']}][{c['faction2_code']}][{c['faction3_code']}]"
        )
    elif "faction2_code" in c:
        return format_text(f"[{c['faction_code']}][{c['faction2_code']}]")
    else:
        return format_text(f"[{c['faction_code']}]")


faction_order = {
    "guardian": "0",
    "seeker": "1",
    "rogue": "2",
    "mystic": "3",
    "survivor": "4",
    "neutral": "5",
    "mythos": "6",
}


def slot_order(c):
    """Returns the slot order of a card."""
    order = {
        "Hand": "1",
        "Hand x2": "2",
        "Arcane": "3",
        "Arcane x2": "4",
        "Accessory": "5",
        "Body": "6",
        "Ally": "7",
        "Tarot": "8",
    }
    if "real_slot" in c:
        if c["real_slot"]:
            slots = c["real_slot"].split(". ")
            if slots[0]:
                return order[slots[0]]
    return "9"


def set_thumbnail_image(c: dict, embed: Embed, back=False) -> None:
    """
    Sets the thumbnail image of an embed, using the card image from ArkhamDB.

    :param c: Card info
    :param embed: Discord Embed
    :param back: If it has to show the card back instead
    :return: None
    """
    if c:
        if "imagesrc" in c:
            if back:
                if "backimagesrc" in c:
                    embed.set_thumbnail(url=f"{ARKHAM_DB}{c['backimagesrc']}")
                else:
                    embed.set_thumbnail(url=f"{ARKHAM_DB}{c['imagesrc']}")
            else:
                embed.set_thumbnail(url=f"{ARKHAM_DB}{c['imagesrc']}")


def format_illustrator(c: dict) -> str:
    """
    Gives the format of the illustrator name of a card.
    :param c: Card info
    :return: String
    """
    if "illustrator" in c:
        return f"🖌 {c['illustrator']}"
    else:
        return ""


def format_name(c: dict) -> str:
    """
    Formats the card's name. Adds the ✱ if the card is unique.
    :param c:
    :return:
    """
    if "is_unique" in c:
        if c["is_unique"]:
            return f"⚹{c['name']}"
    return c["name"]


def format_subtext(c: dict) -> str:
    """
    Formats the subtext of a card, if any.
    :param c:
    :return:
    """
    if "subname" in c:
        return f": _{c['subname']}_"
    else:
        return ""


def color_picker(c: dict) -> int:
    """
    Returns a color according to the card's class.
    :param c:
    :return:
    """
    colors = {
        "survivor": 0xAA2211,
        "rogue": 0x225522,
        "guardian": 0x2255CC,
        "mystic": 0x51479D,
        "seeker": 0xFF7700,
        "neutral": 0xAAAAAA,
        "mythos": 0x333333,
    }
    if "faction2_code" in c:  # Multiclass
        return 0xFFDD55

    return colors[c["faction_code"]]


def format_type(c: dict) -> str:
    """
    Formats the card's type.
    :param c:
    :return:
    """
    if "type_name" in c:
        return f"**{c['type_name']}**"
    return f"**{c['type_code'].capitalize()}**"


def format_traits(c: dict) -> str:
    """
    Format the card's traits if any.
    :param c:
    :return:
    """
    if "traits" in c:
        return f"***{c['traits']}***"
    return ""


def format_flavour(c: dict) -> str:
    """
    Formats the card's flavor text, if any.
    :param c:
    :return:
    """
    if "flavor" in c:
        return f"_{format_text(c['flavor'])}_\n"

    return ""


def format_customizable(c: dict) -> str:
    """
    Format the costumization upgrades, if any.
    :param c:
    :return:
    """

    if "customization_text" in c:
        return f"{format_text(c['customization_text'])}\n"

    return ""


def format_customizable_note(c: dict) -> str:
    """
    Format the costumization upgrades, if any.
    :param c:
    :return:
    """

    if "customization_text" in c:
        return f"_{_('customization_note')}_\n"

    return ""
