import os
from functools import partial
from pathlib import Path

import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars

from ..starting_closing_tests import close_tests, start_tests


def test_settings_change_is_marked(qtbot):  # noqa: PLR0915
    """
    test if load, save and create a new scenario works

    Parameters # noqa: PLR0915
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    assert main_window.dia.windowTitle()[-1] != "*"
    assert main_window.list_widget_scenario.currentItem().text()[-1] != "*"

    main_window.gui_structure.option_font_size.set_value(main_window.gui_structure.option_font_size.get_value() + 1)

    assert main_window.dia.windowTitle()[-1] == "*"
    assert main_window.list_widget_scenario.currentItem().text()[-1] != "*"

    close_tests(main_window, qtbot)
