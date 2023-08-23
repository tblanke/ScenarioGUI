import numpy as np
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning
from ..starting_closing_tests import close_tests, start_tests


def test_float_box_with_units(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    float_units = main_window.gui_structure.float_units
    assert np.isclose(float_units.get_value()[0], float_units.default_value)
    assert np.isclose(float_units.get_value()[1], 0)
    float_units.set_value(((float_units.default_value + 50), 1))
    assert np.isclose((float_units.default_value + 50), float_units.get_value()[0])
    assert np.isclose(1, float_units.get_value()[1])
    float_units.unit_widget.setCurrentIndex(0)
    assert np.isclose((float_units.default_value + 50) * 1000, float_units.get_value()[0])
    assert np.isclose(0, float_units.get_value()[1])
    float_units.set_value(((float_units.default_value + 50), 0))

    assert float_units.check_linked_value((200, None))
    assert float_units.check_linked_value((None, 50))
    assert not float_units.check_linked_value((50, 200))
    assert float_units.check_linked_value((50, 200)) == float_units.create_function_2_check_linked_value((50, 200))()
    float_units.show_option(main_window.gui_structure.int_a, 50, 200)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.int_a.is_hidden()
    float_units.set_value((20, 0))
    float_units.show_option(main_window.gui_structure.int_a, 50, 200)
    assert not main_window.gui_structure.int_a.is_hidden()
    float_units.set_value((220, 0))
    float_units.show_option(main_window.gui_structure.int_a, 50, 200)
    assert not main_window.gui_structure.int_a.is_hidden()
    float_units.add_link_2_show(main_window.gui_structure.int_a, 50, 200)
    float_units.set_value((110, 0))
    assert main_window.gui_structure.int_a.is_hidden()
    float_units.set_value((20, 0))
    assert not main_window.gui_structure.int_a.is_hidden()
    float_units.set_value((220, 0))
    assert not main_window.gui_structure.int_a.is_hidden()
    float_units.unit_widget.setCurrentIndex(1)
    float_units.set_value(20)
    assert float_units.unit_widget.currentIndex() == 0
    assert float_units.widget.value() == 20
    # test set text
    main_window.gui_structure.float_units.set_text("Hello")
    assert main_window.gui_structure.float_units.label.text() == "Hello"
    main_window.save_scenario()
    assert "float_units" in main_window.list_ds[0].to_dict()

    main_window.gui_structure.float_units.add_link_2_show(main_window.gui_structure.filename, 0)

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.float_units.add_link_2_show(main_window.gui_structure.filename, 2)

    close_tests(main_window, qtbot)
