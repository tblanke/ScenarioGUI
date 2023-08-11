from functools import partial

import PySide6.QtWidgets as QtW
import pytest

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.starting_closing_tests import close_tests, start_tests
from tests.test_translations.translation_class import Translations


def test_inheritance_behaviour(qtbot):
    # init gui window
    # init gui window
    main_window = start_tests(qtbot)
    g_s: GUI = main_window.gui_structure
    # add dependencies
    g_s.show_option_under_multiple_conditions(
        g_s.float_f,
        [g_s.float_e, g_s.float_d],
        custom_logic=lambda: g_s.float_d.check_linked_value((20, None)) and not g_s.float_e.is_hidden(),
        check_on_visibility_change=True
    )
    g_s.show_option_under_multiple_conditions(
        g_s.float_e,
        [g_s.float_a, g_s.float_b, g_s.float_c],
        custom_logic=lambda: (g_s.float_a.check_linked_value((20, None)) and g_s.float_b.check_linked_value((20, None))) or g_s.float_c.check_linked_value((20, None)),
        check_on_visibility_change=True
    )
    g_s.float_a.set_value(200)
    assert not g_s.float_a.is_hidden()
    assert not g_s.float_b.is_hidden()
    assert not g_s.float_c.is_hidden()
    assert not g_s.float_d.is_hidden()
    assert g_s.float_e.is_hidden()
    assert g_s.float_f.is_hidden()
    g_s.float_c.set_value(10)
    assert not g_s.float_e.is_hidden()
    assert g_s.float_f.is_hidden()
    g_s.float_d.set_value(10)
    assert not g_s.float_f.is_hidden()
    g_s.float_c.set_value(100)
    assert g_s.float_f.is_hidden()
    close_tests(main_window, qtbot)
