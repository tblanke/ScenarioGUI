import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_text_box(qtbot):
    """
    test text box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)

    assert main_window.gui_structure.text_box.get_value() == main_window.gui_structure.text_box.default_value
    main_window.gui_structure.text_box.set_value("Hello")
    assert main_window.gui_structure.text_box.get_value() == "Hello"

    # test set text
    main_window.gui_structure.text_box.set_text("Hello")
    assert main_window.gui_structure.text_box.label.text() == "Hello"
    main_window.delete_backup()



