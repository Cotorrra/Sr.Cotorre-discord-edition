"""Main bot file"""
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
from sorcery import dict_of

from config import TOKEN
from src.core.translator import lang
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_upgrades, look_for_tarot, refresh_cards, \
    refresh_api_data, look_for_framework, look_for_list_of_cards, look_for_random_player_card, \
    look_for_preview_player_card
from src.response.slash_options import player_card_slash_options, deck_slash_options, \
    general_card_slash_options, tarot_slash_options, timing_slash_options

# pylint: disable=R0913

load_dotenv()
bot = commands.Bot(command_prefix='!SrCotorre')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    """Prints on console that the bot it's ready! It also sets the bot's status."""
    print(f'{bot.user.name} está listo! :parrot:')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name="TSK Previews"))


@slash.slash(name="ah",
             description=lang.locale('ah_description'),
             options=player_card_slash_options())
async def player_card(ctx: SlashContext,
                      name="", level="", faction="",
                      extras="", subtitle="", cycle=""):
    """Handles the /ah slash command, this command returns' player cards."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    embed, hidden = look_for_player_card(query)
    await ctx.send(embed=embed, hidden=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahDeck",
             description=lang.locale('ahDeck_description'),
             options=deck_slash_options())
async def deck(ctx: SlashContext, code, type=""):
    """Handles the /ahDeck command, it returns a deck from ArkhamDB."""
    await ctx.defer()
    embed, hidden = look_for_deck(code, type)
    await ctx.send(embed=embed)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahUp",
             description=lang.locale('ahUp_description'),
             options=deck_slash_options())
async def upgrade(ctx: SlashContext, code, type=""):
    """Handles the /ahUp command, it returns the upgrades of a deck."""
    await ctx.defer()
    embed, hidden = look_for_upgrades(code, type)
    await ctx.send(embed=embed)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahe",
             description=lang.locale('ahe_description'),
             options=general_card_slash_options())
async def encounter(ctx: SlashContext,
                    name="", type="", subtitle="", cycle=""):
    """Handle the /ahe command, it returns encounter cards."""
    # await ctx.defer()
    query = dict_of(name, type, subtitle, cycle)
    embed, hidden = look_for_mythos_card(query)
    await ctx.send(embed=embed, hidden=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahb",
             description=lang.locale('ahb_description'),
             options=general_card_slash_options())
async def back(ctx: SlashContext, name="", type="", subtitle="", cycle=""):
    """Handles the /ahb command, it returns card backs."""
    # await ctx.defer()
    query = dict_of(name, type, subtitle, cycle)
    embed, hidden = look_for_card_back(query)
    await ctx.send(embed=embed, hidden=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahTarot",
             description=lang.locale('ahTarot_description'),
             options=tarot_slash_options())
async def tarot(ctx: SlashContext, name=""):
    """Handles the /ahTarot command, it returns tarot cards."""
    # await ctx.defer()
    embed, hidden = look_for_tarot(name)
    await ctx.send(embed=embed)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahTiming",
             description=lang.locale('ahTiming_description'),
             options=timing_slash_options())
async def game_timing(ctx: SlashContext, timing):
    """Handles the /ahTiming command, it returns game timings."""
    # await ctx.defer()
    embed, hidden = look_for_framework(timing)
    await ctx.send(embed=embed)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahList",
             description=lang.locale('ahList_description'),
             options=player_card_slash_options())
async def list_cards(ctx: SlashContext,
                     name="", level="", faction="",
                     extras="", subtitle="", cycle=""):
    """Handles the /ahList command, it lists playercards."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    embed, hidden = look_for_list_of_cards(query)
    await ctx.send(embed=embed, hidden=hidden)


@slash.slash(name="ahRandom",
             description=lang.locale('ahRandom_description'),
             options=player_card_slash_options())
async def random(ctx: SlashContext,
                 name="", level="", faction="",
                 extras="", subtitle="", cycle=""):
    """Handles the /ahRandom command, it returns a random card."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    embed, hidden = look_for_random_player_card(query)
    await ctx.send(embed=embed, hidden=hidden)


# async def ah_who(ctx: SlashContext, name="", level="", faction="", extras="", subtitle="", cycle=""):
#    ...

@slash.slash(name="ahPreview",
             description=lang.locale('ahPreview_description'),
             options=player_card_slash_options())
async def player_card(ctx: SlashContext,
                      name="", level="", faction="",
                      extras="", subtitle="", cycle=""):
    """Handles the /ah slash command, this command returns' player cards."""
    # await ctx.defer()
    query = dict_of(name, level, faction, extras, subtitle, cycle)
    embed, hidden = look_for_preview_player_card(query)
    await ctx.send(embed=embed, hidden=hidden)
    # await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="refresh",
             description="Refresca las cartas del bot desde ArkhamDB",
             guild_ids=[804912893589585964, 923302104532156449])  # Special Testing Discord
async def refresh_data(ctx: SlashContext):
    """Reloads data from ArkhamDB"""
    await ctx.defer()
    if refresh_cards():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


@slash.slash(name="refreshAPI",
             description="Refresca los datos de la API del bot",
             guild_ids=[804912893589585964, 923302104532156449])
async def refresh_data_api(ctx: SlashContext):
    """Reloads data from the Sr. Cotorre API"""
    await ctx.defer()
    if refresh_api_data():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


bot.run(TOKEN)
