from pathlib import Path, PurePath
import pandas as pd
import numpy as np
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations
from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
import ScenarioGUI.global_settings as global_vars
import keyboard

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_filename_read(qtbot) -> None:
    """
    test filename reading function

    Parameters
    ----------
    qtbot: qtbot
        qtbot
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.save_scenario()
    main_window.gui_structure.filename._init_links()

    folder = Path(__file__).parent.parent
    file = f'{folder.joinpath("./example_data.csv")}'
    assert main_window.gui_structure.filename.get_value() == main_window.gui_structure.filename.default_value
    assert main_window.gui_structure.filename.default_value == file
    # check if no file is passed
    QtC.QTimer.singleShot(1000, lambda: keyboard.press("Esc"))
    main_window.gui_structure.filename.button.click()
    assert main_window.status_bar.widget.currentMessage() == main_window.gui_structure.filename.error_text
    # check file import and calculation
    QtC.QTimer.singleShot(1000, lambda: keyboard.write(file))
    QtC.QTimer.singleShot(1500, lambda: keyboard.press("enter"))
    main_window.gui_structure.filename.button.click()
    assert main_window.gui_structure.filename.get_value() == file.replace("\\", "/")
    assert main_window.gui_structure.filename.check_linked_value(file.replace("\\", "/"))
    main_window.delete_backup()
