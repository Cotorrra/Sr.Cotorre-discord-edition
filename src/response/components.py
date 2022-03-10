import asyncio

from discord_slash import ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle

from src.core.translator import lang


async def cards_buttons_row(bot, ctx, embed):
    # buttons = [create_button(style=ButtonStyle.red, label=lang.locale('self_delete'))]
    # action_row = create_actionrow(*buttons)
    await ctx.send(embed=embed) # , components=[action_row])
    # while True:
    #    try:
    #        button_ctx: ComponentContext = await wait_for_component(bot, components=[action_row], timeout=30)
    #        if button_ctx.author == ctx.author:
    #        break
    #            await button_ctx.origin_message.delete()
    #        await msg.edit(components=None)
    #    except asyncio.TimeoutError:
