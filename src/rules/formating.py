import discord

from src.core.formating import format_text


def format_rule(rule):
    title = f"**{rule['title']}**"
    description = "%s" % format_text(rule['text'])
    return discord.Embed(title=title, description=description, color=0x966e50)
