import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_page(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)

    main_window.gui_structure.page_result.set_text("button name,Name")
    assert main_window.gui_structure.page_result.button.text() == "button name"
    assert main_window.gui_structure.page_result.label.text() == "Name"

    # test linked function which counts the counter every time button is clicked
    assert main_window.gui_structure.counter == 1
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.counter == 2
    main_window.delete_backup()
