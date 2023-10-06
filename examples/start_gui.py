"""
script to start the GUI
"""
# pragma: no cover
from __future__ import annotations

import sys
from json import dump, load
from pathlib import Path
from platform import system
from sys import argv
from sys import exit as sys_exit

import PySide6.QtWidgets as QtW

from examples.example_classes.data_2_class_function import data_2_results
from examples.example_classes.gui_structure import GUI
from examples.example_classes.results_creation_class import ResultsClass
from examples.translation_class_creation.translation_class import Translations
from ScenarioGUI import load_config
from ScenarioGUI.global_settings import FILE_EXTENSION
from ScenarioGUI.gui_classes.gui_combine_window import JsonDict, MainWindow

os_system = system()
is_frozen = getattr(sys, "frozen", False) and os_system == "Windows"  # pragma: no cover


def run(path_list=None):  # pragma: no cover
    load_config(Path("gui_config.ini"))

    # init application
    app = QtW.QApplication()
    # init window
    window = QtW.QMainWindow()
    # init gui window
    main_window = MainWindow(
        window,
        app,
        GUI,
        Translations,
        result_creating_class=ResultsClass,
        data_2_results_function=data_2_results,
    )
    # load file if it is in path list
    if path_list is not None:
        main_window.filename = (
            next(path for path in path_list if path.endswith(f".{FILE_EXTENSION}")),
            0,
        )
        main_window.fun_load_known_filename()

    def export_txt(file_path: Path, data: JsonDict) -> None:
        # write data to back up file
        with open(file_path, "w") as file:
            dump(data, file, indent=1)

    def import_txt(file_path: Path) -> JsonDict:
        # read data from file
        with open(file_path) as file:
            data = load(file)
        return data

    def other_version_import(data: JsonDict) -> JsonDict:
        for dic in data["values"]:
            dic["float_b"] = dic["float_b"] + 10
        return data

    main_window.add_other_export_function("txt", export_txt)
    main_window.add_other_import_function("txt", import_txt)

    main_window.add_other_version_import_function("v0.0.1", other_version_import)
    main_window.activate_load_as_new_scenarios()

    # show window
    window.showMaximized()
    # close app
    sys_exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    # pass system args like a file to read
    run(argv if len(argv) > 1 else None)
