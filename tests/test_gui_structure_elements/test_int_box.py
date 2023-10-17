import numpy as np
import PySide6.QtCore as QtC
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_int_box(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    int_a = main_window.gui_structure.int_a
    assert np.isclose(int_a.get_value(), int_a.default_value)
    int_a.set_value(int_a.default_value + 5)
    assert np.isclose(int_a.default_value + 5, int_a.get_value())

    assert int_a.check_linked_value((20, None))
    assert int_a.check_linked_value((None, 2))
    assert not int_a.check_linked_value((5, 20))
    assert int_a.create_function_2_check_linked_value((None, 50))() == int_a.check_linked_value((None, 50))
    int_a.show_option(main_window.gui_structure.float_b, 5, 20)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(4)
    int_a.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(22)
    int_a.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_a.add_link_2_show(main_window.gui_structure.float_b, below=5, above=20)
    int_a.set_value(10)
    assert main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(4)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(22)
    assert not main_window.gui_structure.float_b.is_hidden()
    main_window.save_scenario()
    assert "int_a" in main_window.list_ds[0].to_dict()
    int_a.widget.setLocale(QtC.QLocale(QtC.QLocale.German, QtC.QLocale.Germany))
    # test validation
    res = int_a.widget.validate("100", 2)
    assert np.isclose(float(res[1].replace(",", ".")), 100)
    assert res[2] == 2
    res = int_a.widget.validate("12345", 2)
    assert np.isclose(float(res[1].replace(",", ".")), 1234)
    assert res[2] == 2
    res = int_a.widget.validate("1.234", 2)
    assert np.isclose(float(res[1].replace(".", "").replace(",", ".")), 1234)
    assert res[1] == "1.234"
    assert res[2] == 2

    int_a.add_link_2_show(main_window.gui_structure.hint_1, below=0)

    with pytest.warns(ConditionalVisibilityWarning):
        int_a.add_link_2_show(main_window.gui_structure.hint_1, below=2)

    close_tests(main_window, qtbot)
