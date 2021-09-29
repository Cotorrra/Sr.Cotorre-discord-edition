import discord

from src.core.formating import format_text
from src.core.translator import locale


def format_tarot(tarot):
    title = f"**{tarot['name']}**"
    up_text = format_text(tarot['up'])
    down_text = format_text(tarot['down'])
    description = f"**{locale('tarot_title')}**" \
                  f"\n\n***{locale('tarot_up_name')}***" \
                  f"\n> _{up_text}_" \
                  f"\n\n***{locale('tarot_down_name')}***" \
                  f"\n> _{down_text}_" \
                  f"\n"
    footnote = f"🖌{tarot['illustrator']}" \
               f"\n{tarot['set']} #{tarot['number']}."
    embed = discord.Embed(title=title, description=description, color=0x000044)
    embed.set_footer(text=footnote)

    return embed
