import os

from dotenv import load_dotenv

# The Bot secret TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Base link to arkhamdb. It varies from language to language
ARKHAM_DB = os.getenv('ARKHAMDB')

# You can choose to es/en: Check Sr-Cotorre Data to check all languages that are available!
LANG = os.getenv('BOT_LANGUAGE')

# You can change where the data comes from
DATA_API = os.getenv('DATA_API')

# Advanced: If you want to change the emojis from the bot
# [tag] -> <emoji:code>
# you can get this code with /:emoji: in Discord.
TEXT_FORMAT = {"[free]": "<:zappyboi:923306654748012644>",
               "[fast]": "<:zappyboi:923306654748012644>",
               "[elder_sign]": "<:elder_sign:923322066378321930>",
               "[wild]": "<:wild:923310032668463124>",
               "[willpower]": "<:willpower:923307352927633498>",
               "[combat]": "<:combat:923307397039140936>",
               "[intellect]": "<:intellect:923307383277645884>",
               "[agility]": "<:agility:923307408447664139>",
               "[action]": "<:action:923307249168941077>",
               "[reaction]": "<:reaction:923307295901880421>",
               "[bless]": "<:bless:923309406848946206>",
               "[curse]": "<:curse:923309369775517756>",
               "[skull]": "<:skull2:923310598580756500>",
               "[cultist]": "<:cultist:923310646454521887>",
               "[tablet]": "<:tablet:923310708391804999>",
               "[elder_thing]": "<:elder_thing:923310743217123399>",
               "[auto_fail]": "<:auto_fail:923310801358577715>",
               "[frost]": "<:frost:923310076373131284>",
               "[mystic]": "<:mystic:923311002710323231>",
               "[seeker]": "<:seeker:923310915191971975>",
               "[guardian]": "<:guardian:923310867481776198>",
               "[rogue]": "<:rogue:923310957269229618>",
               "[survivor]": "<:survivor:923311032494092298>",
               "[neutral]": "<:neutral:923311464209604689>",
               "[mythos]": "<:encounter:923314990872674435>",
               "[health]": "<:health:923311526960590910>",
               "[sanity]": "<:sanity:923312057955287060>",
               "[per_investigator]": "<:per_inv:923312415888773160>",
               "[doom]": "<:doom:923313888055930890>",
               "[clues]": "<:clue:923313866195210320>",
               "[taboo]": "<:taboo:923313941474586684>",
               "<br/>": "\n",
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
