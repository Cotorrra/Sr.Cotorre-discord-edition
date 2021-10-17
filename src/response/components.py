from discord_slash import ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle

from src.core.translator import locale

buttons = [
            create_button(
                style=ButtonStyle.red,
                label=locale('self_destruct')
            ),
          ]
action_row = create_actionrow(*buttons)


async def self_destruct(bot, ctx, user_id):
    button_ctx: ComponentContext = await wait_for_component(bot, components=action_row)
    if user_id == button_ctx.author_id:
        await ctx.message.delete()
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")

