"""Main bot file"""
import interactions
from dotenv import load_dotenv
from sorcery import dict_of
import logging

from config import TOKEN, log_format
from src.core.translator import lang
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_upgrades, look_for_tarot, refresh_cards, \
    refresh_api_data, look_for_framework, look_for_list_of_cards, look_for_random_player_card, \
    look_for_preview_player_card, look_for_whom
from src.response.slash_options import player_card_slash_options, deck_slash_options, \
    general_card_slash_options, tarot_slash_options, timing_slash_options, \
    preview_card_slash_options

# pylint: disable=R0913

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    filename='debug.log',
)

bot = interactions.Client(token=TOKEN)


@bot.event
async def on_ready():
    """Prints on console that the bot it's ready! It also sets the bot's status."""
    print(f'El bot está listo! :parrot:')
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
    #                                                    name="TSK Previews"))


@bot.command(name="ah",
             description=lang.locale('ah_description'),
             options=player_card_slash_options(name_req=True))
async def player_card(ctx: interactions.CommandContext,
                      name, level="", faction="",
                      extras="", subtitle="", cycle=""):
    """Handles the /ah slash command, this command returns' player cards."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    logging.debug(f"/ah sent with: {query}")
    embed, hidden = look_for_player_card(query)
    await ctx.send(embeds=embed, ephemeral=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@bot.command(name="ahdeck",
             description=lang.locale('ahDeck_description'),
             options=deck_slash_options())
async def deck(ctx: interactions.CommandContext, code, type=""):
    """Handles the /ahDeck command, it returns a deck from ArkhamDB."""
    await ctx.defer()
    logging.debug(f"/ahdeck sent with: code={code}, type={type}")
    embed, hidden = look_for_deck(code, type)
    await ctx.send(embeds=embed)


@bot.command(name="ahup",
             description=lang.locale('ahUp_description'),
             options=deck_slash_options())
async def upgrade(ctx: interactions.CommandContext, code, type=""):
    """Handles the /ahUp command, it returns the upgrades of a deck."""
    await ctx.defer()
    logging.debug(f"/ahup sent with: code={code}, type={type}")
    embed, hidden = look_for_upgrades(code, type)
    await ctx.send(embeds=embed)


@bot.command(name="ahe",
             description=lang.locale('ahe_description'),
             options=general_card_slash_options())
async def encounter(ctx: interactions.CommandContext,
                    name="", type="", subtitle="", cycle=""):
    """Handle the /ahe command, it returns encounter cards."""
    # await ctx.defer()
    query = dict_of(name, type, subtitle, cycle)
    logging.debug(f"/ahe sent with: {query}")
    embed, hidden = look_for_mythos_card(query)
    await ctx.send(embeds=embed, ephemeral=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@bot.command(name="ahb",
             description=lang.locale('ahb_description'),
             options=general_card_slash_options())
async def back(ctx: interactions.CommandContext, name="", type="", subtitle="", cycle=""):
    """Handles the /ahb command, it returns card backs."""
    # await ctx.defer()
    query = dict_of(name, type, subtitle, cycle)
    logging.debug(f"/ahb sent with: {query}")
    embed, hidden = look_for_card_back(query)
    await ctx.send(embeds=embed, ephemeral=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@bot.command(name="ahtarot",
             description=lang.locale('ahTarot_description'),
             options=tarot_slash_options())
async def tarot(ctx: interactions.CommandContext, name=""):
    """Handles the /ahTarot command, it returns tarot cards."""
    # await ctx.defer()
    logging.debug(f"/ahtarot sent with: name={name}")
    embed, hidden = look_for_tarot(name)
    await ctx.send(embeds=embed, ephemeral=hidden)


@bot.command(name="ahtiming",
             description=lang.locale('ahTiming_description'),
             options=timing_slash_options())
async def game_timing(ctx: interactions.CommandContext, timing):
    """Handles the /ahTiming command, it returns game timings."""
    # await ctx.defer()
    logging.debug(f"/ahtiming sent with: timing={timing}")
    embed, hidden = look_for_framework(timing)
    await ctx.send(embeds=embed)


@bot.command(name="ahlist",
             description=lang.locale('ahList_description'),
             options=player_card_slash_options())
async def list_cards(ctx: interactions.CommandContext,
                     name="", level="", faction="",
                     extras="", subtitle="", cycle=""):
    """Handles the /ahList command, it lists playercards."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    logging.debug(f"/ahlist sent with: {query}")
    embed, hidden = look_for_list_of_cards(query)
    await ctx.send(embeds=embed, ephemeral=hidden)


@bot.command(name="ahrandom",
             description=lang.locale('ahRandom_description'),
             options=player_card_slash_options())
async def random(ctx: interactions.CommandContext,
                 name="", level="", faction="",
                 extras="", subtitle="", cycle=""):
    """Handles the /ahRandom command, it returns a random card."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    logging.debug(f"/ahrandom sent with: {query}")
    embed, hidden = look_for_random_player_card(query)
    await ctx.send(embeds=embed, ephemeral=hidden)


@bot.command(name="ahwho",
             description=lang.locale('ahWho_description'),
             options=player_card_slash_options(name_req=True))
async def ah_who(ctx: interactions.CommandContext,
                      name, level="", faction="",
                      extras="", subtitle="", cycle=""):
    """Handles the /ah slash command, this command returns' player cards."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    logging.debug(f"/ahWho sent with: {query}")
    embed, hidden = look_for_whom(query)
    await ctx.send(embeds=embed, ephemeral=hidden)
    # await cards_buttons_row(bot, ctx, embed)



@bot.command(name="ahpreview",
             description=lang.locale('ahPreview_description'),
             options=preview_card_slash_options())
async def preview_card(ctx: interactions.CommandContext,
                        card=""):
    """Handles the /ah slash command, this command return's player cards."""
    # await ctx.defer()
    query = dict_of(card)
    logging.debug(f"/ahpreview sent with: {query}")
    embed, hidden = look_for_preview_player_card(query)
    await ctx.send(embeds=embed, ephemeral=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@bot.command(name="refresh",
             description="Refresca las cartas del bot desde ArkhamDB",
             scope=[923302104532156449])  # Special Testing Discord
async def refresh_data(ctx: interactions.CommandContext):
    """Reloads data from ArkhamDB"""
    await ctx.defer()
    if refresh_cards():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


@bot.command(name="refresh_api",
             description="Refresca los datos de la API del bot",
             scope=[923302104532156449])
async def refresh_data_api(ctx: interactions.CommandContext):
    """Reloads data from the Sr. Cotorre API"""
    await ctx.defer()
    if refresh_api_data():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


bot.start()
