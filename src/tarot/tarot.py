import json

from src.core.utils import load_from_repo


def load_tarot():
    """
    Carga el archivo de taboo.
    :return:
    """
    file_src = 'data/tarot/tarot.json'

    info = load_from_repo(file_src)

    info['tarot'] = json.dumps(info['tarot'])
    info['tarot'] = json.loads(info['tarot'])

    return info
