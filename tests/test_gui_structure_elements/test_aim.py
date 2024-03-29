from functools import partial

import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_aim(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    main_window = start_tests(qtbot)
    if not main_window.gui_structure.aim_plot.widget.isChecked():
        main_window.gui_structure.aim_plot.widget.click()

    assert main_window.gui_structure.aim_plot.widget.isChecked()
    main_window.gui_structure.int_a.set_value(201)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.int_a.set_value(100)
    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))

    assert main_window.gui_structure.aim_sub.widget.isChecked()

    main_window.save_scenario()
    main_window.gui_structure.aim_sub.widget.click()
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"

    a = []

    def func(val: list):
        val.append(1)

    main_window.gui_structure.aim_plot.change_event(partial(func, a), also_on_visibility=True)
    assert not main_window.gui_structure.button_box.is_hidden()
    main_window.gui_structure.aim_plot.add_link_2_show(main_window.gui_structure.button_box)
    main_window.gui_structure.aim_add.widget.click()
    assert main_window.gui_structure.button_box.is_hidden()
    main_window.gui_structure.aim_plot.widget.click()
    assert main_window.gui_structure.aim_plot.is_checked()
    assert not main_window.gui_structure.aim_add.is_checked()
    assert not main_window.gui_structure.button_box.is_hidden()

    assert not main_window.gui_structure.aim_plot.is_hidden()
    a_before = len(a)
    main_window.gui_structure.aim_plot.hide()
    assert len(a) == a_before + 1
    assert main_window.gui_structure.aim_plot.is_hidden()
    main_window.gui_structure.aim_plot.show()
    assert len(a) == a_before + 2
    assert not main_window.gui_structure.aim_plot.is_hidden()

    main_window.gui_structure.aim_plot.set_text("Hello")
    assert main_window.gui_structure.aim_plot.widget.text() == "Hello"

    main_window.gui_structure.aim_plot.add_link_2_show(main_window.gui_structure.aim_add)

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.aim_plot.add_link_2_show(main_window.gui_structure.aim_add)

    close_tests(main_window, qtbot)
