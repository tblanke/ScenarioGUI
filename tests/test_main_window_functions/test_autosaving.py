from math import isclose

import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

from ..starting_closing_tests import close_tests, start_tests


def test_autosaving(qtbot):  # noqa: PLR0915
    """
    test if the autosaving saves current changes

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # add two scenarios and set different conductivity
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2.1)
    main_window.gui_structure.option_auto_saving.set_value(1)

    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.change_scenario(0)
    assert 2.1 == main_window.gui_structure.float_b.get_value()
