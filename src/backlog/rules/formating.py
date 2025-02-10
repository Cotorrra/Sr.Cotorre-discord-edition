from interactions import Embed
from src.core.formatting import format_text


def format_rule(rule):
    title = f"**{rule['title']}**"
    description = "%s" % format_text(rule["text"])
    return Embed(title=title, description=description, color=0x966E50)
