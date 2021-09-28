import os

from dotenv import load_dotenv

# The Bot secret TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Base link to arkhamdb. It varies from language to language
arkhamdb = os.getenv('ARKHAMDB')

# You can choose to es/en: Check Sr-Cotorre Data to check what languages are available!
lang = os.getenv('BOT_LANGUAGE')

# Advanced: If you want to change the emojis from the bot
# [tag] -> <emoji:code>
# you can get this code with /:emoji: in Discord.
text_format = {"[free]": "<:Libre:789610643262799913>",
               "[fast]": "<:Libre:789610643262799913>",
               "[elder_sign]": "<:arcano:799004602183843851>",
               "[willpower]": "<:voluntad:830574960510500864>",
               "[combat]": "<:combate:830574960472227870>",
               "[intellect]": "<:intelecto:830574962552209468>",
               "[agility]": "<:agilidad:830574960493461615>",
               "[action]": "<:Accion:789610653912399891>",
               "[reaction]": "<:Reaccion:789610628339073075>",
               "[bless]": "<:bendicion:799051903816171550>",
               "[curse]": "<:maldicion:799050838928654347>",
               "[wild]": "<:Comodin:789619157657583636>",
               "[skull]": "<:calavera:799059800276336721>",
               "[cultist]": "<:sectario:799004435762249729>",
               "[tablet]": "<:tablilla:799004747687526410>",
               "[elder_thing]": "<:primigenio:799059800230461441>",
               "[auto_fail]": "<:fallo:799004322796797953>",
               "[mystic]": "<:Mistico:786679149196476467>",
               "[seeker]": "<:Buscador:786679131768225823>",
               "[guardian]": "<:Guardian:786679100273852457>",
               "[rogue]": "<:Rebelde:786679171257991199>",
               "[survivor]": "<:Superviviente:786679182284947517>",
               "[neutral]": "<:Neutral:786679389303603221>",
               "[mythos]": "<:encuentro:808047457971470388>",
               "[health]": "<:Salud:808821841413668904>",
               "[sanity]": "<:Cordura:808821830608617493>",
               "[per_investigator]": "<:Porinvestigador:789610613650489434>",
               "[doom]": "<:perdicion:801160341886468138>",
               "[clues]": "<:pista:801161173864808548>",
               "</b>": "**",
               "<b>": "**",
               "<em>": "_",
               "</em>": "_",
               "<i>": "_",
               "</i>": "_",
               "<u>": "__",
               "</u>": "__",
               "[[": "***",
               "]]": "***",
               "<cite>": "\n— ",
               "</cite>": "",
               }
