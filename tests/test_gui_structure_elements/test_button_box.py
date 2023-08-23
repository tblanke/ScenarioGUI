import numpy as np
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes import Option
from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_button_box(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)

    button_box = main_window.gui_structure.button_box
    button_box.add_link_2_show(main_window.gui_structure.filename, on_index=1)
    main_window.gui_structure.aim_plot.add_link_2_show(button_box)
    assert np.isclose(button_box.get_value(), button_box.default_value)
    button_box.set_value(button_box.default_value + 1)
    assert np.isclose(button_box.default_value + 1, button_box.get_value())
    assert button_box.check_linked_value(button_box.default_value + 1)
    assert button_box.create_function_2_check_linked_value(button_box.default_value + 1)() == button_box.check_linked_value(button_box.default_value + 1)
    assert not button_box.check_linked_value(button_box.default_value)
    assert button_box.create_function_2_check_linked_value(button_box.default_value)() == button_box.check_linked_value(button_box.default_value)
    button_box.add_link_2_show(main_window.gui_structure.int_a, on_index=0)
    button_box.set_value(button_box.default_value)
    button_box.set_value(button_box.default_value + 1)
    assert main_window.gui_structure.int_a.is_hidden()
    button_box.set_value(button_box.default_value)
    assert not main_window.gui_structure.int_a.is_hidden()
    main_window.save_scenario()
    assert "button_box" in main_window.list_ds[0].to_dict()
    # test if the hidden button box is enabled
    main_window.gui_structure.aim_plot.widget.click() if not main_window.gui_structure.aim_plot.widget.isChecked() else None
    button_box.set_value(button_box.default_value + 1)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.aim_add.widget.click()
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.aim_plot.widget.click()
    button_box.set_value(button_box.default_value)
    main_window.save_scenario()
    assert main_window.list_widget_scenario.count() == 3
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert np.isclose(button_box.default_value + 1, button_box.get_value())
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(2))
    Option.hidden_option_editable = False
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert not button_box.hidden_option_editable
    assert not button_box.frame.isEnabled()
    assert not button_box.widget[0].isEnabled()
    assert np.isclose(button_box.default_value, button_box.get_value())
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(2))
    Option.hidden_option_editable = True
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert np.isclose(button_box.default_value + 1, button_box.get_value())
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(2))
    button_box.hidden_option_editable = False
    assert np.isclose(button_box.default_value, button_box.get_value())
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(2))
    Option.hidden_option_editable = True
    assert not button_box.hidden_option_editable
    button_box.hidden_option_editable = True

    # check that no value error is displayed
    main_window.status_bar.label.setText("")
    button_box.set_value(0)
    assert button_box.get_value() == 0
    button_box.widget[0].click()
    assert button_box.get_value() == 1
    assert main_window.status_bar.label.text() == ""

    button_box.add_link_2_show(main_window.gui_structure.float_b, 1)

    with pytest.warns(ConditionalVisibilityWarning):
        button_box.add_link_2_show(main_window.gui_structure.float_b, 0)
    close_tests(main_window, qtbot)
