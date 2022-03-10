import requests

from config import LANG, DATA_API


def load_rules():
    """
    Carga el archivo de taboo.
    :return:
    """
    params = {"language": LANG,
              "type": "rules"}
    info = requests.get(f'{DATA_API}',
                        params=params).json()

    return info
