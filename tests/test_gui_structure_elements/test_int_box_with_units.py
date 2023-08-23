import numpy as np
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_int_box_with_units(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    int_units = main_window.gui_structure.int_units
    assert np.isclose(int_units.get_value()[0], int_units.default_value)
    assert np.isclose(int_units.get_value()[1], 0)
    int_units.set_value(((int_units.default_value + 5), 1))
    assert np.isclose((int_units.default_value + 5), int_units.get_value()[0])
    assert np.isclose(1, int_units.get_value()[1])
    int_units.unit_widget.setCurrentIndex(0)
    assert np.isclose((int_units.default_value + 5) * 1000, int_units.get_value()[0])
    assert np.isclose(0, int_units.get_value()[1])
    int_units.set_value(((int_units.default_value + 5), 0))

    assert int_units.check_linked_value((20, None))
    assert int_units.check_linked_value((None, 2))
    assert not int_units.check_linked_value((5, 20))
    assert int_units.create_function_2_check_linked_value((5, 20))() == int_units.check_linked_value((5, 20))
    int_units.show_option(main_window.gui_structure.float_b, 5, 20)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.float_b.is_hidden()
    int_units.set_value((4, 0))
    int_units.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_units.set_value((22, 0))
    int_units.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_units.add_link_2_show(main_window.gui_structure.float_b, below=5, above=20)
    int_units.set_value((10, 0))
    assert main_window.gui_structure.float_b.is_hidden()
    int_units.set_value((4, 0))
    assert not main_window.gui_structure.float_b.is_hidden()
    int_units.set_value((22, 0))
    assert not main_window.gui_structure.float_b.is_hidden()
    int_units.unit_widget.setCurrentIndex(1)
    int_units.set_value(20)
    assert int_units.unit_widget.currentIndex() == 0
    assert int_units.widget.value() == 20  # noqa: PLR2004
    main_window.save_scenario()
    assert "int_units" in main_window.list_ds[0].to_dict()

    int_units.add_link_2_show(main_window.gui_structure.hint_1, below=0)

    with pytest.warns(ConditionalVisibilityWarning):
        int_units.add_link_2_show(main_window.gui_structure.hint_1, below=2)

    close_tests(main_window, qtbot)
