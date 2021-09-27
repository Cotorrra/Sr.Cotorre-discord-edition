import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from src.core.translator import locale
from src.e_cards.search import format_query_ec
from src.p_cards.search import format_query_pc
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_upgrades, look_for_tarot
from src.response.utils import player_card_slash_options, deck_slash_options, general_card_slash_options, tarot_slash_options

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!SrCotorre')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo! :parrot:')
    await bot.change_presence(activity=discord.Game('Duolingo'))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=""))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="for e/info"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArkhamDB"))


@slash.slash(name="ah",
             description=locale('ah_description'),
             options=player_card_slash_options())
async def ah_s(ctx, name, level="", faction="", extras="", sub="", pack=""):
    query = format_query_pc(name, level, faction, extras, sub, pack)
    response, embed = look_for_player_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahDeck",
             description=locale('ahDeck_description'),
             options=deck_slash_options())
async def ahMazo_s(ctx, code, type=""):
    response, embed = look_for_deck(code, type)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahUp",
             description=locale('ahUp_description'),
             options=deck_slash_options())
async def ahMejora_s(ctx, code, type=""):
    response, embed = look_for_upgrades(code, type)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahe",
             description=locale('ahe_description'),
             options=general_card_slash_options())
async def ahe_s(ctx, name, type="", sub="", pack=""):
    query = format_query_ec(name, type, sub, pack)
    response, embed = look_for_mythos_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahb",
             description=locale('ahb_description'),
             options=general_card_slash_options())
async def ahback_s(ctx, name, type="", sub="", pack=""):
    query = format_query_ec(name, type, sub, pack)
    response, embed = look_for_card_back(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahTarot",
             description=locale('ahTarot_description'),
             options=tarot_slash_options())
async def ahTarot(ctx, name=""):
    response, embed = look_for_tarot(name)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="InvestigatorTest",
             description="SuperTest",
             guild_ids=[804912893589585964])
async def ahTestPlayer(ctx):
    """
    Sr. Cotorre Lab Only.
    Sends the following cards:
        - Rex Murphy (front and back)
        - Lola Hayes (front and back)
        -
    :param ctx:
    :return:
    """

bot.run(TOKEN)
