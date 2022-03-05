import asyncio

from discord_slash import ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle

from src.core.translator import lang


async def cards_buttons_row(bot, ctx, embed):
    buttons = [create_button(style=ButtonStyle.grey, label=lang.locale('self_delete'), custom_id="delete"),
               create_button(style=ButtonStyle.green, label="wuewuewuewue", custom_id="wuewue")]
    action_row = create_actionrow(*buttons)
    msg = await ctx.send(embed=embed, components=[action_row])
    while True:
        try:
            button_ctx: ComponentContext = await wait_for_component(bot,
                                                                    components=[action_row],
                                                                    timeout=30,
                                                                    check=lambda res: res.author == ctx.author)
            if button_ctx.custom_id == "delete":
                await msg.delete()
                break
            elif button_ctx.custom_id == "wuewue":
                await ctx.send("wuewue", hidden=True)
            else:
                pass
        except asyncio.TimeoutError:
            await msg.edit(components=[])
            break
