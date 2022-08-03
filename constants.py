from pathlib import Path


BASE_DIR: Path = Path(__file__).parent
RESULT_DIR: Path = BASE_DIR / "results" / "csv"
RESULT_DIR.mkdir(exist_ok=True, parents=True)

URL: str = "https://www.detmir.ru/catalog/index/name/lego/"

PATTERN: str = r"Код товара\n(?P<ID>\d+)\nСтрана-производитель\n(?P<country>\w+)"

DT_FORMAT: str = '%d.%m.%Y %H:%M:%S'

LOG_FORMAT: str = "|\t%(asctime)s – [%(levelname)s]: %(message)s. " \
             "Исполняемый файл – '%(filename)s': " \
             "функция – '%(funcName)s'(%(lineno)d)"
