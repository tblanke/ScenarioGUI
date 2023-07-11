from os import remove
from os.path import exists
from pathlib import Path

# from pytestqt import qtbot

import ScenarioGUI.global_settings as globs

import PySide6.QtWidgets as QtW
from matplotlib import pyplot as plt

from ScenarioGUI import load_config
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.gui_structure_classes import ResultFigure

from .gui_structure_for_tests import GUI
from .result_creating_class_for_tests import ResultsClass, data_2_results
from .test_translations.translation_class import Translations

load_config(Path(__file__).absolute().parent.joinpath("./gui_config.ini"))



def start_tests(qtbot) -> MainWindow:
    _backup_filename: str = f"backup.{globs.FILE_EXTENSION}BackUp"
    default_path: Path = Path(Path.home(), f"Documents/{globs.GUI_NAME}")
    backup_file: Path = Path(default_path, _backup_filename)
    if exists(backup_file):  # pragma: no cover
        remove(backup_file)
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    return main_window


def close_tests(main_window: MainWindow, qtbot) -> None:
    [ds.close_figures() for ds in main_window.list_ds]
    [plt.close(cat.fig) for cat in main_window.gui_structure.page_result.list_categories if isinstance(cat, ResultFigure)]
    if main_window.saving_threads:  # pragma: no cover
        qtbot.wait(100)
        _ = [thread.terminate() for thread in main_window.saving_threads]
