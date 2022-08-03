from pathlib import Path


BASE_DIR = Path(__file__).parent

URL = "https://www.detmir.ru/catalog/index/name/lego/page/{}/"

PATTERN = r"Код товара\n(?P<ID>\d+)\nСтрана-производитель\n(?P<country>\w+)"
