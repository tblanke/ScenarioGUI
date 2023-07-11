from functools import partial

import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.starting_closing_tests import close_tests, start_tests
from tests.test_translations.translation_class import Translations


def test_show_multiple_under_conditions(qtbot):
    # init gui window
    # init gui window
    main_window = start_tests(qtbot)
    g_s: GUI = main_window.gui_structure
    g_s.show_option_under_multiple_conditions(
        g_s.float_b,
        [g_s.aim_add, g_s.int_a],
        functions_check_for_and=[
            g_s.aim_add.widget.isChecked,
            partial(g_s.int_a.check_linked_value, (None, 50)),
        ],
    )
    g_s.aim_add.widget.click() if not g_s.aim_add.widget.isChecked() else None
    g_s.int_a.set_value(55)
    assert g_s.aim_add.widget.isChecked()
    assert g_s.int_a.check_linked_value((None, 50))
    assert not g_s.float_b.is_hidden()
    g_s.int_a.set_value(40)
    assert g_s.float_b.is_hidden()
    g_s.int_a.set_value(55)
    assert not g_s.float_b.is_hidden()
    g_s.aim_sub.widget.click()
    assert not g_s.aim_add.widget.isChecked()
    assert g_s.float_b.is_hidden()
    g_s.int_a.set_value(40)
    assert g_s.float_b.is_hidden()

    g_s.show_option_under_multiple_conditions(
        g_s.text_box,
        [g_s.aim_sub, g_s.int_a],
        functions_check_for_or=[
            g_s.aim_sub.widget.isChecked,
            partial(g_s.int_a.check_linked_value, (None, 20)),
        ],
    )

    g_s.int_a.set_value(25)
    assert g_s.aim_sub.widget.isChecked()
    assert g_s.int_a.check_linked_value((None, 20))
    assert not g_s.text_box.is_hidden()
    g_s.int_a.set_value(15)
    assert not g_s.text_box.is_hidden()
    g_s.int_a.set_value(25)
    assert not g_s.text_box.is_hidden()
    g_s.aim_add.widget.click()
    assert not g_s.aim_sub.widget.isChecked()
    assert not g_s.text_box.is_hidden()
    g_s.int_a.set_value(15)
    assert g_s.text_box.is_hidden()

    g_s.show_option_under_multiple_conditions(
        g_s.float_units,
        [g_s.aim_plot, g_s.int_small_1, g_s.int_small_2],
        functions_check_for_or=[
            g_s.aim_plot.widget.isChecked,
            partial(g_s.int_small_1.check_linked_value, (None, 20)),
        ],
        functions_check_for_and=[partial(g_s.int_small_2.check_linked_value, (26, None))],
    )
    g_s.int_small_2.set_value(20)
    g_s.int_small_1.set_value(21)
    g_s.aim_plot.widget.click()
    assert g_s.aim_plot.widget.isChecked()
    assert g_s.int_small_2.check_linked_value((26, None))
    assert g_s.int_small_1.check_linked_value((None, 20))
    assert not g_s.float_units.is_hidden()
    g_s.int_small_2.set_value(27)
    assert not g_s.int_small_2.check_linked_value((26, None))
    assert g_s.float_units.is_hidden()
    g_s.int_small_2.set_value(20)
    assert not g_s.float_units.is_hidden()
    g_s.int_small_1.set_value(18)
    assert not g_s.float_units.is_hidden()
    g_s.int_small_1.set_value(21)
    assert not g_s.float_units.is_hidden()
    g_s.aim_add.widget.click()
    assert not g_s.float_units.is_hidden()
    g_s.int_small_1.set_value(18)
    assert g_s.float_units.is_hidden()
    close_tests(main_window, qtbot)
