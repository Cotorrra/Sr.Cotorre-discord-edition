import interactions
from dotenv import load_dotenv
from sorcery import dict_of

from config import TOKEN
from src.core.translator import lang
from src.response.response import look_for_mythos_card, look_for_player_card, \
    look_for_deck, look_for_card_back, look_for_upgrades, look_for_tarot, refresh_cards, refresh_api_data, \
    look_for_framework, look_for_list_of_cards, look_for_random_player_card
from src.response.slash_options import player_card_slash_options, deck_slash_options, general_card_slash_options, \
    tarot_slash_options, timing_slash_options

load_dotenv()
bot = interactions.Client(token=TOKEN)


@bot.event
async def on_ready():
    print(f'Sr. Cotorre está listo! :parrot:')
    # await bot.change_presence(activity=discord.Game(''))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="🦜"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="for e/info"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArkhamDB"))


@bot.command(name="ah",
             description=lang.locale('ah_description'),
             options=player_card_slash_options())
async def ah(ctx: interactions.CommandContext, name="", level="", faction="", extras="", sub="", pack=""):
    await ctx.defer()
    embed, hidden = look_for_player_card(query)
    await ctx.send(embed=embed)


@bot.command(name="ahDeck",
             description=lang.locale('ahDeck_description'),
             options=deck_slash_options())
async def ah_mazo_s(ctx: interactions.CommandContext, code, type=""):
    await ctx.defer()
    embed, hidden = look_for_deck(code, type)
    await ctx.send(embed=embed)


@bot.command(name="ahUp",
             description=lang.locale('ahUp_description'),
             options=deck_slash_options())
async def ah_mejora_s(ctx: interactions.CommandContext, code, type=""):
    await ctx.defer()
    embed, hidden = look_for_upgrades(code, type)
    await ctx.send(embed=embed)


@bot.command(name="ahe",
             description=lang.locale('ahe_description'),
             options=general_card_slash_options())
async def ahe_s(ctx: interactions.CommandContext, name, type_="", sub="", pack=""):
    await ctx.defer()
    embed, hidden = look_for_mythos_card(query)
    await ctx.send(embed=embed)


@bot.command(name="ahb",
             description=lang.locale('ahb_description'),
             options=general_card_slash_options())
async def ahback_s(ctx: interactions.CommandContext, name, type_="", sub="", pack=""):
    await ctx.defer()
    embed, hidden = look_for_card_back(query)
    await ctx.send(embed=embed)


@bot.command(name="ahTarot",
             description=lang.locale('ahTarot_description'),
             options=tarot_slash_options())
async def ah_tarot(ctx: interactions.CommandContext, name=""):
    await ctx.defer()
    embed, hidden = look_for_tarot(name)
    await ctx.send(embed=embed)


# SOONtm
@bot.command(name="ahTiming",
             description=lang.locale('ahTiming_description'),
             options=timing_slash_options())
async def ah_timing(ctx: interactions.CommandContext, timing):
    await ctx.defer()
    embed, hidden = look_for_framework(timing)
    await ctx.send(embed=embed)


@bot.command(name="ahList",
             description=lang.locale('ahList_description'),
             options=player_card_slash_options())
async def ah_list(ctx: interactions.CommandContext, name="", level="", faction="", extras="", sub="", pack=""):
    await ctx.defer()
    query =  dict_of(name, level, faction, extras, sub, pack)
    embed, hidden = look_for_list_of_cards(query)
    await ctx.send(embed=embed)


@bot.command(name="ahRandom",
             description=lang.locale('ahRandom_description'),
             options=player_card_slash_options())
async def ah_random(ctx: interactions.CommandContext, name="", level="", faction="", extras="", sub="", pack=""):
    await ctx.defer()
    query =  dict_of(name, level, faction, extras, sub, pack)
    embed, hidden = look_for_random_player_card(query)
    await ctx.send(embed=embed)


async def ah_who(ctx: interactions.CommandContext, name="", level="", faction="", extras="", sub="", pack=""):
    ...


@bot.command(name="refresh",
             description="Refresca las cartas del bot desde ArkhamDB",
             scope=923302104532156449)  # Special Testing Discord
async def refresh_data(ctx: interactions.CommandContext):
    await ctx.defer()
    if refresh_cards():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


@bot.command(name="refreshAPI",
             description="Refresca los datos de la API del bot",
             scope=923302104532156449)
async def refresh_data(ctx: interactions.CommandContext):
    await ctx.defer()
    if refresh_api_data():
        await ctx.send("Refrescado!")
    else:
        await ctx.send("<:confusedwatermelon:739425223358545952>")


bot.start()
