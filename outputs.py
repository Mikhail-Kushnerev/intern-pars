import csv
from pathlib import Path

from constants import RESULT_DIR


def write_csv(result: dict[str, list[str]]):
    file_name: Path = RESULT_DIR / "result.csv"
    with open(file_name, mode="a", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, dialect="unix", delimiter=";")
        if not Path(file_name).exists():
            writer.writerow(
                ("ID Товара", "Наименование", "Актуальная цена", "Город", "Старая цена", "URL")
            )
        for key in result:
            row: list[str] = result[key]
            string: tuple[str, ...] = (
                (row[3], key, row[1], row[-1], row[2], row[0])
            )
            writer.writerow(string)
