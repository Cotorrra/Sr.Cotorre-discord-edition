import json

from config import lang
from src.core.utils import load_from_repo


def load_language(lang: str):
    """
    Load the language file
    :return:
    """
    file_src = f'data/lang/{lang}.json'

    info = load_from_repo(file_src)

    info['lang'] = json.dumps(info['lang'])
    info['lang'] = json.loads(info['lang'])

    return info


def locale(tag):
    return curr_lang['lang'][tag]


curr_lang = load_language(lang)