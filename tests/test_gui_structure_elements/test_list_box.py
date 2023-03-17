import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_list_box(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    # test set value
    assert main_window.gui_structure.list_small_2.get_value() == main_window.gui_structure.list_small_2.default_value
    main_window.gui_structure.list_small_2.set_value(main_window.gui_structure.list_small_2.default_value + 1)
    assert main_window.gui_structure.list_small_2.get_value() == main_window.gui_structure.list_small_2.default_value + 1
    # test links
    main_window.gui_structure.list_small_2.set_value(0)
    assert main_window.gui_structure.hint_2.is_hidden()
    main_window.gui_structure.list_small_2.set_value(1)
    assert not main_window.gui_structure.hint_2.is_hidden()
    # test set text
    main_window.gui_structure.list_box.set_text("Hello,4,5,6,7")
    assert main_window.gui_structure.list_box.label.text() == "Hello"
    for i, val in zip(range(4), ["4", "5", "6", "7"], strict=True):
        assert main_window.gui_structure.list_box.widget.itemText(i) == val

    main_window.delete_backup()
