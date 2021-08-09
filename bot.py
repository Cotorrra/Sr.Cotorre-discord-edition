import os

import discord
import requests
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from src.decks.search import format_query_deck
from src.e_cards.search import format_query_ec
from src.p_cards.search import format_query_pc
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_faq, look_for_upgrades, look_for_rule
from src.response.utils import player_card_slash_options, deck_slash_options, general_card_slash_options, \
    rules_slash_options

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!SrCotorre')
slash = SlashCommand(bot, sync_commands=True)

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo! :parrot:')
    # await bot.change_presence(activity=discord.Game('a'))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for e/info"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="for e/info"))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArkhamDB"))


@slash.slash(name="ah",
             description="Busca cartas de jugador en ArkhamDB.",
             options=player_card_slash_options())
async def ah_s(ctx, *args):
    query = format_query_pc(ctx.kwargs)
    response, embed = look_for_player_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahMazo",
             description="Muestra mazos de ArkhamDB.",
             options=deck_slash_options())
async def ahMazo_s(ctx, *args):
    query, deck_type = format_query_deck(ctx.kwargs)
    response, embed = look_for_deck(query, deck_type)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahMejora",
             description="Muestra la mejora de un mazo de ArkhamDB.",
             options=deck_slash_options())
async def ahMejora_s(ctx, *args):
    query, deck_type = format_query_deck(ctx.kwargs)
    response, embed = look_for_upgrades(query, deck_type)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahe",
             description="Busca cartas de encuentros en ArkhamDB.",
             options=general_card_slash_options())
async def ahe_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    response, embed = look_for_mythos_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahFAQ",
             description="Busca FAQs en cartas.",
             options=general_card_slash_options())
async def ahfaq_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    response, embed = look_for_faq(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahReglas",
             description="Busca Reglas/Conceptos del manual del juego.",
             options=rules_slash_options())
async def ahReglas_s(ctx, *args):
    query = ctx.kwargs.get('regla')
    response, embed = look_for_rule(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahb",
             description="Busca el texto de partes traseras de cartas.",
             options=general_card_slash_options())
async def ahback_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    response, embed = look_for_card_back(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


bot.run(TOKEN)
