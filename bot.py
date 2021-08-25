import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from src.e_cards.search import format_query_ec
from src.p_cards.search import format_query_pc
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_faq, look_for_upgrades, look_for_rule, look_for_tarot
from src.response.utils import player_card_slash_options, deck_slash_options, general_card_slash_options, \
    rules_slash_options, tarot_slash_options

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!SrCotorre')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} está listo! :parrot:')
    await bot.change_presence(activity=discord.Game('leer el Tarot'))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for e/info"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="for e/info"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArkhamDB"))


@slash.slash(name="ah",
             description="Busca cartas de jugador en ArkhamDB.",
             options=player_card_slash_options())
async def ah_s(ctx, nombre, nivel="", clase="", extras="", subtitulo="", pack=""):
    query = format_query_pc(nombre, nivel, clase, extras, subtitulo, pack)
    response, embed = look_for_player_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahMazo",
             description="Muestra mazos de ArkhamDB.",
             options=deck_slash_options())
async def ahMazo_s(ctx, codigo, tipo=""):
    response, embed = look_for_deck(codigo, tipo)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahMejora",
             description="Muestra la mejora de un mazo de ArkhamDB.",
             options=deck_slash_options())
async def ahMejora_s(ctx, codigo, tipo=""):
    response, embed = look_for_upgrades(codigo, tipo)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahe",
             description="Busca cartas de encuentros en ArkhamDB.",
             options=general_card_slash_options())
async def ahe_s(ctx, nombre, tipo="", subtitulo="", pack=""):
    query = format_query_ec(nombre, tipo, subtitulo, pack)
    response, embed = look_for_mythos_card(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahFAQ",
             description="Busca FAQs en cartas.",
             options=general_card_slash_options())
async def ahfaq_s(ctx, nombre, tipo="", subtitulo="", pack=""):
    query = format_query_ec(nombre, tipo, subtitulo, pack)
    response, embed = look_for_faq(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahReglas",
             description="Busca Reglas/Conceptos del manual del juego.",
             options=rules_slash_options())
async def ahReglas_s(ctx, regla):
    response, embed = look_for_rule(regla)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahb",
             description="Busca el texto de partes traseras de cartas.",
             options=general_card_slash_options())
async def ahback_s(ctx, nombre, tipo="", subtitulo="", pack=""):
    query = format_query_ec(nombre, tipo, subtitulo, pack)
    response, embed = look_for_card_back(query)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


@slash.slash(name="ahTarot",
             description="Busca cartas Tarot del Regreso al Circulo Roto",
             options=tarot_slash_options())
async def ahTarot(ctx, nombre=""):
    response, embed = look_for_tarot(nombre)
    if embed:
        await ctx.send(response, embed=embed)
    else:
        await ctx.send(response)


bot.run(TOKEN)
