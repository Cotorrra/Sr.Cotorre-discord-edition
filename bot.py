import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from config import TOKEN
from src.core.translator import locale
from src.e_cards.search import format_query_ec
from src.p_cards.search import format_query_pc
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_upgrades, look_for_tarot, refresh_cards
from src.response.utils import player_card_slash_options, deck_slash_options, general_card_slash_options, tarot_slash_options

load_dotenv()
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
    embed = look_for_player_card(query)
    await ctx.send(embed=embed)


@slash.slash(name="ahDeck",
             description=locale('ahDeck_description'),
             options=deck_slash_options())
async def ah_mazo_s(ctx, code, type=""):
    embed = look_for_deck(code, type)
    await ctx.send(embed=embed)


@slash.slash(name="ahUp",
             description=locale('ahUp_description'),
             options=deck_slash_options())
async def ah_mejora_s(ctx, code, type=""):
    await ctx.defer()
    embed = look_for_upgrades(code, type)
    await ctx.send(embed=embed)


@slash.slash(name="ahe",
             description=locale('ahe_description'),
             options=general_card_slash_options())
async def ahe_s(ctx, name, type="", sub="", pack=""):
    query = format_query_ec(name, type, sub, pack)
    embed = look_for_mythos_card(query)
    await ctx.send("", embed=embed)


@slash.slash(name="ahb",
             description=locale('ahb_description'),
             options=general_card_slash_options())
async def ahback_s(ctx, name, type="", sub="", pack=""):
    query = format_query_ec(name, type, sub, pack)
    embed = look_for_card_back(query)
    await ctx.send("", embed=embed)


@slash.slash(name="ahTarot",
             description=locale('ahTarot_description'),
             options=tarot_slash_options())
async def ahTarot(ctx, name=""):
    embed = look_for_tarot(name)
    await ctx.send("", embed=embed)


@slash.slash(name="refresh",
             description="Refresca las cartas del bot",
             guild_ids=[804912893589585964])  # Special Testing Discord
async def refresh_data(ctx):
    await ctx.defer()
    if refresh_cards():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")

bot.run(TOKEN)
