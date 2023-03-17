import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_function_button(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.res = 0

    # test function call
    def func():
        main_window.res += 5

    main_window.gui_structure.function_button.change_event(func)
    assert main_window.res == 0
    main_window.gui_structure.function_button.button.click()
    assert main_window.res == 5
    # test set text
    main_window.gui_structure.function_button.set_text("Hello")
    assert main_window.gui_structure.function_button.button.text() == "Hello"
    # check show and hide function
    main_window.gui_structure.function_button.show()
    assert not main_window.gui_structure.function_button.is_hidden()
    main_window.gui_structure.function_button.hide()
    assert main_window.gui_structure.function_button.is_hidden()
