import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashCommand, ComponentContext, ButtonStyle, SlashContext
from discord_slash.utils.manage_components import wait_for_component, create_actionrow, create_button
from dotenv import load_dotenv

from config import TOKEN
from src.core.translator import lang
from src.e_cards.search import format_query_ec
from src.p_cards.search import format_query_pc
# from src.response.components import self_destruct, buttons
from src.response.components import cards_buttons_row
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_upgrades, look_for_tarot, refresh_cards, refresh_api_data
from src.response.slash_options import player_card_slash_options, deck_slash_options, general_card_slash_options, \
    tarot_slash_options, timing_slash_options

load_dotenv()
bot = commands.Bot(command_prefix='!SrCotorre')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo! :parrot:')
    # await bot.change_presence(activity=discord.Game(''))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Buttons"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="for e/info"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArkhamDB"))


@slash.slash(name="ah",
             description=lang.locale('ah_description'),
             options=player_card_slash_options())
async def ah_s(ctx: SlashContext, name, level="", faction="", extras="", sub="", pack=""):
    await ctx.defer()
    query = format_query_pc(name, level, faction, extras, sub, pack)
    embed = look_for_player_card(query)

    await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahDeck",
             description=lang.locale('ahDeck_description'),
             options=deck_slash_options())
async def ah_mazo_s(ctx, code, type=""):
    await ctx.defer()
    embed = look_for_deck(code, type)
    await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahUp",
             description=lang.locale('ahUp_description'),
             options=deck_slash_options())
async def ah_mejora_s(ctx, code, type=""):
    await ctx.defer()
    embed = look_for_upgrades(code, type)
    await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahe",
             description=lang.locale('ahe_description'),
             options=general_card_slash_options())
async def ahe_s(ctx, name, type="", sub="", pack=""):
    await ctx.defer()
    query = format_query_ec(name, type, sub, pack)
    embed = look_for_mythos_card(query)
    await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahb",
             description=lang.locale('ahb_description'),
             options=general_card_slash_options())
async def ahback_s(ctx, name, type="", sub="", pack=""):
    await ctx.defer()
    query = format_query_ec(name, type, sub, pack)
    embed = look_for_card_back(query)
    await cards_buttons_row(bot, ctx, embed)


@slash.slash(name="ahTarot",
             description=lang.locale('ahTarot_description'),
             options=tarot_slash_options())
async def ahTarot(ctx, name=""):
    await ctx.defer()
    embed = look_for_tarot(name)
    await cards_buttons_row(bot, ctx, embed)


"""
# SOONtm
@slash.slash(name="ahTiming",
             description=lang.locale('ahTiming_description'),
             options=timing_slash_options())
async def ahTiming(ctx):
    await ctx.defer()
    embed = look_for_framework()
    await cards_buttons_row(bot, ctx, embed)
"""


@slash.slash(name="refresh",
             description="Refresca las cartas del bot",
             guild_ids=[804912893589585964, 923302104532156449])  # Special Testing Discord
async def refresh_data(ctx):
    await ctx.defer()
    if refresh_cards():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


@slash.slash(name="refreshAPI",
             description="Refresca los datos de la API del bot",
             guild_ids=[804912893589585964, 923302104532156449])
async def refresh_data(ctx):
    await ctx.defer()
    if refresh_api_data():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


bot.run(TOKEN)
