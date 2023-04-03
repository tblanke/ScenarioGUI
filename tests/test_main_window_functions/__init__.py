from pathlib import Path

import pytest

from ScenarioGUI.global_settings import load
import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


@pytest.fixture(autouse=True, scope='session')
def run_before_and_after_tests(qtbot):
    """Fixture to execute asserts before and after a test is run"""
    load(Path(".").absolute().joinpath("./tests/gui_config.ini"))
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()

    yield main_window  # this is where the testing happens

    # Teardown : fill with any logic you want
    main_window.delete_backup()