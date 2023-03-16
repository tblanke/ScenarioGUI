"""
script to create the translation class from csv file
"""
from __future__ import annotations

from os import system
from typing import TYPE_CHECKING

from pandas import read_csv

from .global_settings import FOLDER

if TYPE_CHECKING:
    from pathlib import Path


def translate_csv_2_class(csv_file_with_path: str | Path, target_path: str | Path):
    d_f = read_csv(csv_file_with_path, sep=";", encoding="utf-8")

    file_name = FOLDER.joinpath(f"{target_path}/translation_class.py")

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("from typing import List\n")
        file.write("class Translations:  # pragma: no cover\n")
        list_of_options = d_f["name"].to_list()
        list_of_options.append("languages")
        text = f"__slots__ = {tuple(list_of_options)}"
        file.write(f"\t{text}\n")
        file.write("\tdef __init__(self):\n")
        file.write(f"\t\tself.languages: List[str] = {d_f.columns[1:].to_list()}\n")
        for name, translations in zip(d_f["name"], d_f.iloc[:, 1:].to_numpy(), strict=True):
            text = f"self.{name}: list[str] = {translations.tolist()}"
            file.write(f"\t\t{text}\n")

    system(f"py -m black --line-length 160 {file_name}")
