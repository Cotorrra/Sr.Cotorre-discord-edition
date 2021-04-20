import os

import discord
import requests
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from e_cards.search import format_query_ec
from p_cards.search import format_query_pc
from response.response import help_short, help_long, player_card_slash_options, general_card_slash_options, \
    deck_slash_options, look_for_rule, rules_slash_options, look_for_mythos_card, look_for_player_card, \
    look_for_card_back, look_for_deck, look_for_upgrades, look_for_faq

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!a')
slash = SlashCommand(bot, sync_commands=True)

ah_all_cards = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=1').json()

ah_player = requests.get('https://es.arkhamdb.com/api/public/cards?encounter=0').json()

# Encounter p_cards include: Special player p_cards, Weaknesses, enemies, acts, plans, etc.
ah_encounter = [c for c in ah_all_cards if "spoiler" in c]


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo para usarse c:')
    await bot.change_presence(activity=discord.Game('hacer /'))


@bot.command(name='hhelp')
async def send_help_short(ctx):
    await ctx.send(embed=help_short())


@bot.command(name='hhelpme')
async def send_help(ctx):
    await ctx.send(embed=help_long())


@bot.command(name='hback')
async def ahback(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    response, embed = look_for_card_back(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hj')
async def ahj(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    response, embed = look_for_player_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hd')
async def ahd(ctx, code: str):
    response, embed = look_for_deck(code)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hm')
async def ahm(ctx, code: str):
    query = ' '.join(ctx.message.content.split()[1:])
    response, embed = look_for_mythos_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hu')
async def ahu(ctx, code):
    response, embed = look_for_upgrades(code)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hp')
async def ahp(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    response, embed = look_for_faq(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@bot.command(name='hr')
async def ahr(ctx):
    query = ' '.join(ctx.message.content.split()[1:])
    response, embed = look_for_rule(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


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
             description="Muestra tu mazo de ArkhamDB.",
             options=deck_slash_options())
async def ahMazo_s(ctx, *args):
    query = ctx.kwargs.get('id')
    response, embed = look_for_deck(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahMejora",
             description="Muestra la mejora de tu mazo de ArkhamDB.",
             options=deck_slash_options())
async def ahMejora_s(ctx, *args):
    query = ctx.kwargs.get('id')
    response, embed = look_for_upgrades(query)
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
             description="Busca Reglas/Conceptos del juego.",
             options=rules_slash_options())
async def ahReglas_s(ctx, *args):
    query = ctx.kwargs.get('regla')
    response, embed = look_for_rule(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahb",
             description="Busca las partes traseras de cartas.",
             options=general_card_slash_options())
async def ahback_s(ctx, *args):
    query = format_query_ec(ctx.kwargs)
    response, embed = look_for_card_back(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


bot.run(TOKEN)
