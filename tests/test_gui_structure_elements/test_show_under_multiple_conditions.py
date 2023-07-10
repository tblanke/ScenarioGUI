from functools import partial

import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations


def test_results_text(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    g_s: GUI = main_window.gui_structure
    g_s.show_option_under_multiple_conditions(g_s.float_b, [g_s.aim_add, g_s.int_a],
                                              functions_check_for_and=[g_s.aim_add.widget.isChecked, partial(g_s.int_a.check_linked_value,
                                                                                                             (None, 50
                                                                                                              ))])
    g_s.aim_add.widget.click() if not g_s.aim_add.widget.isChecked() else None
    g_s.int_a.set_value(55)
    assert g_s.aim_add.widget.isChecked()
    assert g_s.int_a.check_linked_value((None, 50))
    assert not g_s.float_b.is_hidden()
    g_s.int_a.set_value(40)
    assert g_s.float_b.is_hidden()
    g_s.int_a.set_value(55)
    assert not g_s.float_b.is_hidden()
    g_s.aim_add.widget.click()
    assert not g_s.aim_add.widget.isChecked()
    assert g_s.float_b.is_hidden()
    main_window.delete_backup()
