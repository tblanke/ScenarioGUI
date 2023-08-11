from functools import partial

import PySide6.QtWidgets as QtW
import pytest

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.starting_closing_tests import close_tests, start_tests
from tests.test_translations.translation_class import Translations


def test_show_under_multiple_conditions_on_result_page(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    g_s: GUI = main_window.gui_structure
    main_window.delete_backup()
    main_window = start_tests(qtbot)
    g_s: GUI = main_window.gui_structure
    g_s.show_option_under_multiple_conditions(
        g_s.result_depending_visibility,
        [g_s.aim_plot, g_s.int_small_1, g_s.int_small_2],
        custom_logic=lambda:(g_s.aim_plot.widget.isChecked() or g_s.int_small_1.check_linked_value((None, 20))) and g_s.int_small_2.check_linked_value((26, None))
                             )
    g_s.int_small_2.set_value(20)
    g_s.int_small_1.set_value(21)
    g_s.aim_plot.widget.click()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    assert not g_s.result_depending_visibility.is_hidden()

    g_s.int_small_2.set_value(27)
    assert g_s.result_depending_visibility.is_hidden()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert g_s.result_depending_visibility.is_hidden()
    g_s.int_small_2.set_value(20)
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert not g_s.result_depending_visibility.is_hidden()
    g_s.int_small_1.set_value(18)
    # assert g_s.result_depending_visibility.is_hidden()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert not g_s.result_depending_visibility.is_hidden()
    g_s.int_small_1.set_value(21)
    # assert g_s.result_depending_visibility.is_hidden()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert not g_s.result_depending_visibility.is_hidden()
    g_s.aim_add.widget.click()
    # assert g_s.result_depending_visibility.is_hidden()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert not g_s.result_depending_visibility.is_hidden()
    g_s.int_small_1.set_value(18)
    # assert g_s.result_depending_visibility.is_hidden()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert g_s.result_depending_visibility.is_hidden()
    close_tests(main_window, qtbot)
