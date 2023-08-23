from functools import partial

import pytest
from pytest import raises

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning
from tests.gui_structure_for_tests import GUI
from tests.starting_closing_tests import close_tests, start_tests


def test_show_multiple_under_conditions(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    g_s: GUI = main_window.gui_structure
    g_s.show_option_under_multiple_conditions(
        g_s.float_b,
        [g_s.aim_add, g_s.int_a],
        functions_check_for_and=[
            g_s.aim_add.widget.isChecked,
            g_s.int_a.create_function_2_check_linked_value((None, 50)),
        ],
    )
    g_s.aim_add.widget.click() if not g_s.aim_add.widget.isChecked() else None
    g_s.int_a.set_value(55)
    assert g_s.aim_add.widget.isChecked()
    assert g_s.int_a.check_linked_value((None, 50))
    assert not g_s.float_b.is_hidden()
    g_s.int_a.set_value(40)
    assert not g_s.int_a.check_linked_value((None, 50))
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
        custom_logic=lambda: (g_s.aim_plot.widget.isChecked() or g_s.int_small_1.check_linked_value((None, 20)))
        and g_s.int_small_2.check_linked_value((26, None)),
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
    with raises(UserWarning):
        g_s.show_option_under_multiple_conditions(
            g_s.float_units,
            [g_s.aim_plot, g_s.int_small_1, g_s.int_small_2],
            custom_logic=lambda: (g_s.aim_plot.widget.isChecked() or g_s.int_small_1.check_linked_value((None, 20))),
            functions_check_for_and=[
                g_s.aim_add.widget.isChecked,
                partial(g_s.int_a.check_linked_value, (None, 50)),
            ],
        )

    with pytest.warns(ConditionalVisibilityWarning):
        g_s.show_option_under_multiple_conditions(
            g_s.float_units,
            [g_s.aim_plot, g_s.int_small_1, g_s.int_small_2],
            custom_logic=lambda: (g_s.aim_plot.widget.isChecked() or g_s.int_small_1.check_linked_value((None, 20)))
            and g_s.int_small_2.check_linked_value((26, None)),
        )

    close_tests(main_window, qtbot)


def test_show_multiple_under_conditions_multiple_options(qtbot):  # noqa: PLR0915
    # init gui window
    # init gui window
    main_window = start_tests(qtbot)
    g_s: GUI = main_window.gui_structure
    g_s.show_option_under_multiple_conditions(
        [g_s.float_b, g_s.float_a],
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
    assert not g_s.float_a.is_hidden()
    g_s.int_a.set_value(40)
    assert g_s.float_b.is_hidden()
    assert g_s.float_a.is_hidden()
    g_s.int_a.set_value(55)
    assert not g_s.float_b.is_hidden()
    assert not g_s.float_a.is_hidden()
    g_s.aim_sub.widget.click()
    assert not g_s.aim_add.widget.isChecked()
    assert g_s.float_b.is_hidden()
    assert g_s.float_a.is_hidden()
    g_s.int_a.set_value(40)
    assert g_s.float_b.is_hidden()
    assert g_s.float_a.is_hidden()

    g_s.show_option_under_multiple_conditions(
        [g_s.text_box, g_s.float_c],
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
    assert not g_s.float_c.is_hidden()
    g_s.int_a.set_value(15)
    assert not g_s.text_box.is_hidden()
    assert not g_s.float_c.is_hidden()
    g_s.int_a.set_value(25)
    assert not g_s.text_box.is_hidden()
    assert not g_s.float_c.is_hidden()
    g_s.aim_add.widget.click()
    assert not g_s.aim_sub.widget.isChecked()
    assert not g_s.text_box.is_hidden()
    assert not g_s.float_c.is_hidden()
    g_s.int_a.set_value(15)
    assert g_s.text_box.is_hidden()
    assert g_s.float_c.is_hidden()

    g_s.show_option_under_multiple_conditions(
        [g_s.float_units, g_s.float_d],
        [g_s.aim_plot, g_s.int_small_1, g_s.int_small_2],
        custom_logic=lambda: (g_s.aim_plot.widget.isChecked() or g_s.int_small_1.check_linked_value((None, 20)))
        and g_s.int_small_2.check_linked_value((26, None)),
    )
    g_s.int_small_2.set_value(20)
    g_s.int_small_1.set_value(21)
    g_s.aim_plot.widget.click()
    assert g_s.aim_plot.widget.isChecked()
    assert g_s.int_small_2.check_linked_value((26, None))
    assert g_s.int_small_1.check_linked_value((None, 20))
    assert not g_s.float_units.is_hidden()
    assert not g_s.float_d.is_hidden()
    g_s.int_small_2.set_value(27)
    assert not g_s.int_small_2.check_linked_value((26, None))
    assert g_s.float_units.is_hidden()
    assert g_s.float_d.is_hidden()
    g_s.int_small_2.set_value(20)
    assert not g_s.float_units.is_hidden()
    assert not g_s.float_d.is_hidden()
    g_s.int_small_1.set_value(18)
    assert not g_s.float_units.is_hidden()
    assert not g_s.float_d.is_hidden()
    g_s.int_small_1.set_value(21)
    assert not g_s.float_units.is_hidden()
    assert not g_s.float_d.is_hidden()
    g_s.aim_add.widget.click()
    assert not g_s.float_units.is_hidden()
    assert not g_s.float_d.is_hidden()
    g_s.int_small_1.set_value(18)
    assert g_s.float_units.is_hidden()
    assert g_s.float_d.is_hidden()
    close_tests(main_window, qtbot)
