import numpy as np
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_multiple_int_box(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    multiple_ints = main_window.gui_structure.multiple_ints
    assert np.allclose(multiple_ints.get_value(), multiple_ints.default_value)
    multiple_ints.set_value((multiple_ints.default_value[0] + 5, multiple_ints.default_value[1] + 5, multiple_ints.default_value[2] + 5))
    assert np.allclose((multiple_ints.default_value[0] + 5, multiple_ints.default_value[1] + 5, multiple_ints.default_value[2] + 5), multiple_ints.get_value())

    assert multiple_ints.check_linked_value((20, None))
    assert multiple_ints.check_linked_value((None, 2))
    assert not multiple_ints.check_linked_value((5, 20))
    assert multiple_ints.create_function_2_check_linked_value((5, 20))() == multiple_ints.check_linked_value((5, 20))
    multiple_ints.show_option(main_window.gui_structure.float_b, 5, 20)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((4, 6, 7))
    multiple_ints.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((6, 7, 22))
    multiple_ints.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    multiple_ints.add_link_2_show(main_window.gui_structure.float_b, below=5, above=20)
    multiple_ints.set_value((10, 11, 12))
    assert main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((4, 6, 7))
    assert not main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((6, 22, 7))
    assert not main_window.gui_structure.float_b.is_hidden()
    main_window.save_scenario()
    assert "multiple_ints" in main_window.list_ds[0].to_dict()

    multiple_ints.add_link_2_show(main_window.gui_structure.hint_1, below=(0, 0, 0))

    with pytest.warns(ConditionalVisibilityWarning):
        multiple_ints.add_link_2_show(main_window.gui_structure.hint_1, below=(0, 0, 0))

    close_tests(main_window, qtbot)
