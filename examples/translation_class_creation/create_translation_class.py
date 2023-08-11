from pathlib import Path

from ScenarioGUI.translation_csv_to_py import translate_csv_2_class


def main():  # pragma: no cover
    folder: Path = Path(__file__).parent
    translate_csv_2_class(folder.joinpath("Translations.csv"), folder)


if __name__ == "__main__":  # pragma: no cover
    main()
